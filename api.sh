if ! [ -x "$(uvicorn api:app --host 127.0.0.1 --port 1929)" ]; then
	echo 'Error: uvicorn is not installed.' >&2
	pip install fastapi uvicorn[standard]
	exit 1
else
	uvicorn api:app --host 127.0.0.1 --port 1929 --reload
fi
