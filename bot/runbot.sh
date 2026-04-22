while true; do
    source venv/bin/activate
    python main.py

    echo "Script crashed. Restarting..."
    sleep 1
done