from flask import Flask, request, make_response
import hashlib
from weixin_api import WXBizMsgCrypt
app = Flask(__name__)
app.config['DEBUG'] = True

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.
weixin_api_handle = WXBizMsgCrypt()
wexin_api_handle.__init__('xiangqinxiangai', 'mUlWiBFcToJrNIoey6V7a21Lp2Owku8v0UbmPl0BnfH', 'wxc3fb21835d599831')

@app.route('/',methods=['GET','POST'])
def wechat_auth():
    # token
    if request.method == 'GET':
        token='xiangqinxiangai'
        data = request.args
        signature = data.get('signature','')
        timestamp = data.get('timestamp','')
        nonce = data.get('nonce','')
        echostr = data.get('echostr','')
        s = [timestamp,nonce,token]
        s.sort()
        s = ''.join(s)
        if (hashlib.sha1(s).hexdigest() == signature):
            return make_response(echostr)
    else:
        data = request.args
        signature = data.get('signature', '')
        timestamp = data.get('timestamp', '')
        nonce = data.get('nonce', '')
        rec = request.stream.read()
        ret, xml_rec = weixin_api_handle.DecryptMsg(rec, signature, timestamp, nonce)
        # xml_rec = ET.fromstring(rec)
        msgtype = xml_rec.find('MsgType').text
        tou = xml_rec.find('ToUserName').text
        fromu = xml_rec.find('FromUserName').text
        xml_rep_img = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[news]]></MsgType><ArticleCount>1</ArticleCount><Articles><item><Title><![CDATA[%s]]></Title><Description><![CDATA[%s]]></Description><PicUrl><![CDATA[%s]]></PicUrl></item></Articles><FuncFlag>1</FuncFlag></xml>"

        # 如效果.png中所示的图文消息
        xml_rep_mutiimg = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[news]]></MsgType><ArticleCount>6</ArticleCount><Articles><item><Title><![CDATA[%s]]></Title><PicUrl><![CDATA[%s]]></PicUrl></item><item><Title><![CDATA[我的冰箱]]></Title><Url><![CDATA[%s]]></Url></item><item><Title><![CDATA[定制早餐]]></Title><Url><![CDATA[%s]]></Url></item><item><Title><![CDATA[定制午餐]]></Title><Url><![CDATA[%s]]></Url></item><item><Title><![CDATA[定制晚餐]]></Title><Url><![CDATA[%s]]></Url></item><item><Title><![CDATA[结伴购物]]></Title><Url><![CDATA[%s]]></Url></item></Articles></xml>"

        # 用户一旦关注改公众账号，自动回复以下图文消息
        if msgtype == "event":
            msgcontent = xml_rec.find('Event').text
            if msgcontent == "subscribe":
                msgcontent = "欢迎来到！"
            else:
                msgcontent = "Bye Bye"
            msg_title = u"美食助手，您的私人定制"
            msg_imag_url = "http://gourmetmaster.sinaapp.com/static/main_meitu_3.jpg"
            response = make_response(
                xml_rep_img % (fromu, tou, str(int(time.time())), msg_title, msgcontent, msg_imag_url))
            response.content_type = 'application/xml'
            return response
            # 用户任意发消息，自动回复
        else:
            content = xml_rec.find('Content').text
            home_title = "主人好，我是一只满血满蓝的营养师 && 厨师，今天起我将是您的私人美食助手~"
            my_imag_url = "http://gourmetmaster.sinaapp.com/static/main_meitu_3.jpg"
            # 以下5个url,在该文件中分别有实现其具体响应的部分，见本文件开头的五个@app.route
            fridgeurl = "http://gourmetmaster.sinaapp.com/fridge"
            breakfasturl = "http://gourmetmaster.sinaapp.com/breakfast"
            dinnerurl = "http://gourmetmaster.sinaapp.com/dinner"
            supperurl = "http://gourmetmaster.sinaapp.com/supper"
            shoptogether = "http://gourmetmaster.sinaapp.com/shoptogether"
            # 点击每项，转到相应的url
            response = make_response(xml_rep_mutiimg % (
            fromu, tou, str(int(time.time())), fromu, my_imag_url, fridgeurl, breakfasturl, dinnerurl, supperurl,
            shoptogether))
            response.content_type = 'application/xml'
            return response
        return render_template("helper_parent.html", messages=messages, comments=comments)

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
