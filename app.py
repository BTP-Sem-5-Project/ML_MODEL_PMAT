from flask import Flask,request,jsonify
from flask_cors import CORS, cross_origin
from scipy.spatial import distance

app = Flask(__name__)

CORS(app, support_credentials=True)

@app.route("/rank_devs",methods=["POST"])
@cross_origin()
def rank_devs():
    # print("############################")
    desired_skills = request.json['desired_skills'].split(' ')
    candidates = request.json['candidates']

    desired_skills = [x.lower() for x in desired_skills]

    # print(desired_skills)
    # print(candidates)

    for i in range(len(candidates)):
        candidates[i]['mat']=[]
        candidates[i]['skills'] = [x.lower() for x in candidates[i]['skills']]
        for skill in desired_skills:
            if skill in candidates[i]['skills']:
                candidates[i]['mat'].append(1)
            else:
                candidates[i]['mat'].append(0)

    # print(candidates)

    desired_matrix = [1 for x in desired_skills]

    # print(desired_matrix)

    for i in range(len(candidates)):
        if candidates[i]['mat'] != [0]*len(desired_skills):
            candidates[i]['similarity'] = 1 - distance.cosine(candidates[i]['mat'],desired_matrix)
        else:
            candidates[i]['similarity'] = 0
    # print(candidates)

    candidates = sorted(candidates,key = lambda x:x['similarity'],reverse=True)
    # print("Sorted List")
    # for i in candidates:
    #     print(i)
    
    return jsonify(ranklist = candidates)

@app.route("/health_check", methods=["GET"])
@cross_origin()
def health_check():
    return "API Up And Running"

# Default port:
if __name__ == "__main__":
    app.run()