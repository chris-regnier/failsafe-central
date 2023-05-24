if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src:get_app", host="", port=8000, factory=True, reload=True)
