server-dev:
    flask --app gvet run --debug
    
server-test:
    pytest

[working-directory:"client"]
client-dev:
    npm run dev

[working-directory:"client"]
build:
    npm run build
    rm -rf ../gvet/static/assets
    cp -r ./dist/assets ../gvet/static

