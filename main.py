from starlette.applications import Starlette
from starlette.routing import Route, WebSocketRoute
from starlette.responses import PlainTextResponse, JSONResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.testclient import TestClient
from starlette.websockets import WebSocket

async def homepage(request):
    #return  JSONResponse({"name":"John Doe"}) 
    return JSONResponse({"name":"John Doe"})  #PlainTextResponse("Hello, It's an example of middleware implementation!")

async def websocket_endpoint(websocket: WebSocket):
    await  websocket.accept()

    while True:
        try:

            data = await websocket.receive_text()
            print(f"Recived message: {data}")

            await websocket.send_text(f"Message text was: {data}")
        except Exception as e:
            print(f"connection error : {e}")
            break
    await websocket.close()

routes = [
    Route('/', homepage),
    WebSocketRoute("/ws", websocket_endpoint),
]

# Create the Starlette app
app = Starlette(routes=routes)


app.add_middleware(CORSMiddleware, allow_origins=["*"])


def test_homepage():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.text == "Hello, This is an example of Testing & Debugging!"
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1",port=8000)
