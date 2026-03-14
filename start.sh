#!/bin/bash

ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "Starting Resume Modifier..."
echo ""

# Kill any existing processes on the ports
lsof -ti:8000 | xargs kill -9 2>/dev/null
lsof -ti:5173 | xargs kill -9 2>/dev/null

# Start backend using explicit venv paths (no cd needed)
echo "Backend starting on http://localhost:8000"
"$ROOT/backend/venv/bin/uvicorn" main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --reload \
    --app-dir "$ROOT/backend" \
    > /tmp/resume_backend.log 2>&1 &
BACKEND_PID=$!

# Start frontend
echo "Frontend starting on http://localhost:5173"
cd "$ROOT/frontend" && npm run dev > /tmp/resume_frontend.log 2>&1 &
FRONTEND_PID=$!

# Wait for backend to be ready
echo ""
echo "Waiting for servers..."
for i in {1..15}; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        break
    fi
    sleep 1
done

echo ""
echo "Both servers running!"
echo "  Backend:  http://localhost:8000"
echo "  Frontend: http://localhost:5173"
echo ""
echo "Logs:"
echo "  Backend:  tail -f /tmp/resume_backend.log"
echo "  Frontend: tail -f /tmp/resume_frontend.log"
echo ""
echo "Press Ctrl+C to stop."

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo 'Stopped.'" EXIT
wait
