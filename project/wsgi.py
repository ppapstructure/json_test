from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

# confing.py에서 docker용인지 local용인지 구분 잘해서 경로수정할것.