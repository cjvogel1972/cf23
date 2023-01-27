import os
import json
import openai
import pandas as pd

from flask import Flask, jsonify, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=("GET", "POST"))
def email():
    return render_template("index.html")

@app.route("/email", methods=("GET", "POST"))
def index():
    return render_template("email.html")


@app.route("/chat", methods=("GET", "POST"))
def chat():
    if request.method == "POST":
        dynatrace_data = dynatrace_pod_data()
        weblogic_1_data = weblogic_pod_1()
        weblogic_2_data = weblogic_pod_2()
        ase_dashboard_data = ase_dashboard()
        fpl_dashboard_data = fpl_dashboard()

        prompt_list = [request.form["prompt"]] + [ase_dashboard_data] + [fpl_dashboard_data]


        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=" ".join(prompt_list),
            max_tokens=256,
            temperature=0.7,
            echo=False,

        )
        conclusion = response.choices[0].text
        print(f"Conclusion: {conclusion}")

        # Send the response back
        return jsonify(request.form["prompt"], conclusion)


def dynatrace_pod_data():
    df = pd.read_csv("pod_data_logresults-2023-01-26-10_41_56.csv")
    df.to_json(r"pod_data_logresults-2023-01-26-10_41_56.json")
    dynatrace_pod_file = open("pod_data_logresults-2023-01-26-10_41_56.json", "r")
    dynatrace_pod_obj = json.load(dynatrace_pod_file)
    return json.dumps(dynatrace_pod_obj)
def weblogic_pod_1():
    df = pd.read_csv("logresults-2023-01-26 10_13_03.csv")
    df.to_json(r"logresults-2023-01-26 10_13_03.json")
    weblogic_pod_1_file = open("logresults-2023-01-26 10_13_03.json", "r")
    weblogic_pod_1_obj = json.load(weblogic_pod_1_file)
    return json.dumps(weblogic_pod_1_obj)

def weblogic_pod_2():
    weblogic_pod_2_file = open("logresults-2023-01-26 10_13_40.json", "r")
    weblogic_pod_2_obj = json.load(weblogic_pod_2_file)
    return json.dumps(weblogic_pod_2_obj)

def ase_dashboard():
    ase_dashboard_file = open("ASE-proposalweb-dashboard.json", "r")
    ase_dashboard_obj = json.load(ase_dashboard_file)
    return json.dumps(ase_dashboard_obj, separators=(',', ':'))

def fpl_dashboard():
    fpl_dashboard_file = open("FPL-dashboard.json", "r")
    fpl_dashboard_obj = json.load(fpl_dashboard_file)
    return json.dumps(fpl_dashboard_obj, separators=(',', ':'))