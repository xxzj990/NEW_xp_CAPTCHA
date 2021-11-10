#!/usr/bin/env python
# -*- conding:utf-8 -*-
from http.server import HTTPServer, BaseHTTPRequestHandler
import muggle_ocr
import re,time,base64,os

host = ('0.0.0.0', 8899)

class Resquest(BaseHTTPRequestHandler):
    def handler(self):
        self.wfile.write(self.rfile.readline())

    def do_GET(self):
        self.send_error(404, "Page not Found!")

    def do_POST(self):
        #print(self.headers)
        #print(self.command)
        text = ''
        try:
            if self.path != '/base64':
                self.send_error(404, "Page not Found!")
                return

            img_name = time.time()
            req_datas = self.rfile.read(int(self.headers['content-length']))
            req_datas = req_datas.decode()
            base64_img = re.search('base64=(.*?)$',req_datas)
            #print(base64_img.group(1)) #post base64参数的内容

            with open("temp/%s.png"%img_name, 'wb') as f:
                f.write(base64.b64decode(base64_img.group(1)))
                f.close()

            #验证码识别
            sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.Captcha)
            with open(r"temp/%s.png"%img_name, "rb") as f:
                b = f.read()
            text = sdk.predict(image_bytes=b)
            print('\n'+text+'\n') #识别的结果

            #删除掉图片文件，以防占用太大的内存
            os.remove("temp/%s.png"%img_name)
        except:
            text= '0000'
            print('\n识别失败！\n')
        
        if text =='':
            text= '0000'
            print('\n识别失败！\n')

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(text.encode('utf-8'))

if __name__ == '__main__':
    os.makedirs('temp', exist_ok=True)
    with open('temp/log.txt', 'w') as f:
        pass
    server = HTTPServer(host, Resquest)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()
