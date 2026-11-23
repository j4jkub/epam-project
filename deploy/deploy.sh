
set -euo pipefail
cd "$(dirname "$0")/.."

export AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test AWS_DEFAULT_REGION=us-east-1
ENDPOINT="${ENDPOINT:-http://localhost:4566}"
A="aws --endpoint-url=$ENDPOINT"

until curl -sf "$ENDPOINT/_ministack/health" >/dev/null; do sleep 2; done

# --- build images ---
docker build -t myapi:local ./backend

docker build -t fe-build -f frontend/Dockerfile.s3 frontend
rm -rf frontend/dist
cid=$(docker create fe-build)
docker cp "$cid:/app/dist" frontend/dist
docker rm "$cid"

# --- S3 ---
$A s3 mb s3://uploads  || true
$A s3 mb s3://frontend || true
$A s3 sync frontend/dist s3://frontend --delete

# --- RDS ---
if ! $A rds describe-db-instances --db-instance-identifier appdb >/dev/null 2>&1; then
  $A rds create-db-instance \
    --db-instance-identifier appdb --engine postgres --engine-version 15 \
    --master-username app --master-user-password secret123 \
    --db-name app --db-instance-class db.t3.micro --allocated-storage 20
fi

# find the container and the HOST port Docker published for Postgres
DB_PORT=""
DB_CONTAINER=""
for i in $(seq 1 60); do
  DB_CONTAINER=$(docker ps --filter "name=instance-appdb" --format "{{.Names}}" | head -n1)
  if [ -n "$DB_CONTAINER" ]; then
    DB_PORT=$(docker port "$DB_CONTAINER" 5432/tcp 2>/dev/null | head -n1 | sed 's/.*://')
  fi
  [[ "$DB_PORT" =~ ^[0-9]+$ ]] && break
  sleep 2
done
[[ "$DB_PORT" =~ ^[0-9]+$ ]] || { echo "Could not find published Postgres port"; exit 1; }
echo "Postgres host port: $DB_PORT"

# wait until Postgres accepts connections
for i in $(seq 1 30); do
  docker exec "$DB_CONTAINER" pg_isready -U app -d app >/dev/null 2>&1 && break
  sleep 2
done

# --- ECS ---
$A ecs create-cluster --cluster-name app || true

# stop old tasks so port 8000 is free
for t in $($A ecs list-tasks --cluster app --query 'taskArns[]' --output text); do
  $A ecs stop-task --cluster app --task "$t" >/dev/null
done

cat > deploy/taskdef.json <<EOF
{
  "family": "api",
  "containerDefinitions": [{
    "name": "api",
    "image": "myapi:local",
    "essential": true,
    "portMappings": [{"containerPort": 8000, "hostPort": 8000}],
    "environment": [
      {"name": "URL_DATABASE", "value": "postgresql+psycopg2://app:secret123@host.docker.internal:${DB_PORT}/app"},
      {"name": "UPLOAD_BUCKET", "value": "uploads"},
      {"name": "FRONTEND_ORIGIN", "value": "http://localhost:4566"},
      {"name": "AWS_ACCESS_KEY_ID", "value": "test"},
      {"name": "AWS_SECRET_ACCESS_KEY", "value": "test"},
      {"name": "AWS_DEFAULT_REGION", "value": "us-east-1"},
      {"name": "SECRET_KEY", "value": "dev-secret-change-me"},
      {"name": "ALGORITHM", "value": "HS256"},
      {"name": "ACCESS_TOKEN_EXPIRE_MINUTES", "value": "30"}
    ]
  }]
}
EOF
cat deploy/taskdef.json | sed 's/secret123/***/'

$A ecs register-task-definition --cli-input-json file://deploy/taskdef.json >/dev/null
$A ecs run-task --cluster app --task-definition api >/dev/null

echo "App: http://localhost:4566/frontend/index.html"
echo "API: http://localhost:8000/docs"