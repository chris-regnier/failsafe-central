from . import App

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(App, host="", port=8000)
