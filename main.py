from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import ocr

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
async def index():
    return {'message': 'Team Pawang OCR Service'}


@app.post('/receipt', status_code=200)
async def receipt(file: UploadFile):
    image = await file.read()
    try:
        data = ocr.get_string(image)
        data = ocr.text_preprocessing(data)
        amount = ocr.find_amount(data)
        if amount == None:
            raise Exception('Amount not found, please try again')
        return {'status': True, 'amount': amount}
    except Exception as e:
        raise HTTPException(status_code=400, detail={
                            'status': False, 'message': str(e)})
