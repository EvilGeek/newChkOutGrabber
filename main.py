import itertools, base64, re, requests 

from flask import *

app=Flask(__name__)

app.secret_key="wolfHoVaixD"

def decode_base64(encoded_string):

    decoded_bytes = base64.b64decode(encoded_string)

    decoded_string = decoded_bytes.decode('utf-8')

    return decoded_string

def getPK(html):

    regex="pk_live_[0-9a-zA-Z]{99}|pk_live_[0-9a-zA-Z]{34}|pk_live_[0-9a-zA-Z]{24}"

    try:

        return re.findall(regex, html)[0]

    except Exception as e:

        return "Not Found"

def getRawData(pk, cs):

    h={

    "Host": "api.stripe.com",

    "sec-ch-ua": "\"Chromium\";v\u003d\"112\", \"Google Chrome\";v\u003d\"112\", \"Not:A-Brand\";v\u003d\"99\"",

    "accept": "application/json",

    "content-type": "application/x-www-form-urlencoded",

    "dnt": "1",

    "sec-ch-ua-mobile": "?1",

    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",

    "sec-ch-ua-platform": "\"Android\"",

    "origin": "https://checkout.stripe.com",

    "sec-fetch-site": "same-site",

    "sec-fetch-mode": "cors",

    "sec-fetch-dest": "empty",

    "referer": "https://checkout.stripe.com/",

    "accept-language": "en-IN,en-GB;q\u003d0.9,en-US;q\u003d0.8,en;q\u003d0.7,hi;q\u003d0.6"

    }

    data=f"key={pk}&eid=NA&browser_locale=en-IN&redirect_type=url"

    url=f"https://api.stripe.com/v1/payment_pages/{cs}/init"

    req=requests.post(url, data=data, headers=h)

    if req.status_code==200:

        return req.json()

    return None

def getEmail(raw):

    email=raw.get("customer_email", "Not Found")

    return str(email)

def getAmt(raw):

    try:

        amt=raw.get("line_item_group", {}).get("line_items", [{}])[0].get("total", "Not Found")

        return str(amt)

    except:

        return "Not Found"

def getCurrency(raw):

    try:

        c=raw.get("line_item_group", {}).get("currency", "Not Found")

        return c

    except:

        return "Not Found"

def getCS(url):

  return url.split("/")[5].split("#")[0]

def xor_decode(ciphertext):

    key = itertools.cycle([5])

    plaintext = ''.join(chr(ord(c) ^ next(key)) for c, k in zip(ciphertext, key))

    return plaintext

def getHash(url):

    ok=url.split("#")

    print(ok, url)

    return ok[len(ok)-1]

@app.route("/")
def home():
    return "@WolfieEXE <3"

@app.route("/api/grabber/", methods=["POST", "GET"])

@app.route("/api/grabber", methods=["POST", "GET"])

def GrabberApi():

    if request.form.get("url"):

        url=request.form.get("url")

        try:

            ok=getHash(url)

          #  print(ok)

            hashh=xor_decode(decode_base64(ok.replace("%2F", "/").replace("%2B","+")))

            cs=getCS(url)

            pk=getPK(hashh)

            raw=getRawData(pk, cs)

            if raw==None:

                return jsonify(status=False, msg="Session Expired.")

            email, amt, currency=getEmail(raw), getAmt(raw), getCurrency(raw)

            return jsonify(status=True, pk=pk, cs=cs, email=email, amt=amt, currency=currency)

        except Exception as e:

            print(e)

            return jsonify(status=False, msg="Invalid Checkout Link.")

    else:

      return jsonify(status=False, msg="Checkout Link Not Found, Pass it as a postdata.")

if __name__=="__main__":

    app.run(hreaded=True)
