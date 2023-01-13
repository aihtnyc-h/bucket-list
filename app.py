from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient("mongodb+srv://test:sparta@cluster0.orldv4f.mongodb.net/Cluster0?retryWrites=true&w=majority")
db = client.dbsparta

@app.route('/')
def home():
   return render_template('bucket.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form['bucket_give']
    bucket_list = list(db.bucket.find({}, {'_id': False}))
    count = len(bucket_list) + 1

    doc = {
        'num':count,
        'bucket':bucket_receive,
        'done':0
    }
    db.bucket.insert_one(doc)

    return jsonify({'msg': '등록 완료!'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    num_receive = request.form['num_give']
    db.bucket.update_one({'num':int(num_receive)}, {'$set': {'done': 1}})

    return jsonify({'msg': '버킷 완료 :)'})

@app.route("/bucket", methods=["GET"])
def bucket_get():
    bucket_list = list(db.bucket.find({}, {'_id': False}))

    return jsonify({'buckets': bucket_list})

# 취소하기
@app.route("/bucket/cancel", methods=["post"])
def bucket_cancel():
    num_receive = request.form['num_give']
    db.bucket.update_one({'num': int(num_receive)}, {'$set': {'done': 0}})

    #틀린 코드!! 왜틀렷는지
    #db.bucket.cancel_one({'num': int(num_receive)}),

    return jsonify({'msg':"취소 완료"})


if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)