test:
    pytest -m "not integration"

full-test:
    pytest

start:
    flask --app gvet run --debug


[working-directory:"client"]
start-client:
    npm run dev

[working-directory:"client"]
build:
    npm run build
    rm -rf ../gvet/static/bundles
    cp -r ./dist/bundles ../gvet/static
