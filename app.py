from flask import Flask, Blueprint, render_template, request, jsonify, redirect, url_for
from CPU_Processes import Process
from FCFS import FCFS
from SJF import SJF
from PriorityNP import PriorityNP
from PriorityP import PriorityP
from RoundRobin import RoundRobin
from SRTF import SRTF
from MLQ import MLQ
from MLFQ import MLFQ
from PageReplacement import PageReplacement
from Cryptography import encrypt_my_algo, decrypt_my_algo
from DiskScheduling import DiskScheduling

# from views import views

# app = Flask(__name__)
# app.register_blueprint(views, url_prefix="/views")


app = Flask(__name__)


@app.route("/")
def cpuScheduling():
    return render_template("cpuScheduling.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/pageReplacement")
def pageReplacement():
    return render_template("pageReplacement.html")


@app.route("/cryptography")
def cryptography():
    return render_template("cryptography.html")


@app.route("/diskScheduling")
def diskScheduling():
    return render_template("diskScheduling.html")


@app.route("/sendInputCPUScheduling", methods=["POST"])
def handle_user_input_CPU_scheduling():
    # try:
    data = request.get_json()

    # Process the data as needed
    main_algorithm = data.get("main_algorithm")
    arrival_time = data.get("arrival_time")
    burst_time = data.get("burst_time")
    priority = data.get("priority") or None
    quantum_time = data.get("quantum_time") or None
    mlfq_qt = data.get("mlfq_qt") or []
    mlfq_algorithm = data.get("mlfq_algorithm") or None
    mlq_algorithms = data.get("mlq_algorithms") or []
    level = data.get("level") or None

    print(priority)

    AT = [int(x) for x in arrival_time.split()]
    BT = [int(x) for x in burst_time.split()]
    P = [int(x) for x in priority.split()] if priority else None
    L = [int(x) for x in level.split()] if level else None

    # Construct the processes_list
    processes_list = [
        [f"P{i + 1}", AT[i] if i < len(AT) else 0, BT[i] if i < len(BT) else 0]
        for i in range(len(BT))
    ]

    if P:
        for i in range(len(processes_list)):
            processes_list[i].append(P[i])
    if L:
        for i in range(len(processes_list)):
            processes_list[i].append(L[i])

    print(processes_list)

    if main_algorithm == "FCFS":
        pInfo = Process("FCFS")
        pInfo.processes_list = processes_list
        pInfo.multi_check = pInfo.prio_check = False
        pInfo.trimProcessList()
        print("FCFS:")
        FCFS(pInfo)
        return jsonify(
            data=[pInfo.timestamps, pInfo.orderOfProcesses, pInfo.processes_list]
        )
    elif main_algorithm == "SJF":
        pInfo2 = Process("SJF")
        pInfo2.processes_list = processes_list
        pInfo2.multi_check = pInfo2.prio_check = False
        pInfo2.trimProcessList()
        print("\n\nSJF:")
        SJF(pInfo2)
        return jsonify(
            data=[pInfo2.timestamps, pInfo2.orderOfProcesses, pInfo2.processes_list]
        )
    elif main_algorithm == "PriorityNP":
        pInfo3 = Process("PriorityNP")
        pInfo3.processes_list = processes_list
        pInfo3.multi_check = False
        pInfo3.trimProcessList()
        print("\n\nPriority (Non-Preemptive):")
        PriorityNP(pInfo3)
        return jsonify(
            data=[pInfo3.timestamps, pInfo3.orderOfProcesses, pInfo3.processes_list]
        )
    elif main_algorithm == "PriorityP":
        pInfo4 = Process("PriorityP")
        pInfo4.processes_list = processes_list
        pInfo4.multi_check = False
        pInfo4.trimProcessList()
        print("\n\nPriority (Preemptive):")
        PriorityP(pInfo4)
        return jsonify(
            data=[pInfo4.timestamps, pInfo4.orderOfProcesses, pInfo4.processes_list]
        )
    elif main_algorithm == "RoundRobin":
        pInfo5 = Process("Round-Robin")
        pInfo5.processes_list = processes_list
        pInfo5.QT = int(quantum_time)
        pInfo5.multi_check = pInfo5.prio_check = False
        pInfo5.trimProcessList()
        print(f"\n\nRound Robin (Quantum Time: {pInfo5.QT}):")
        RoundRobin(pInfo5)
        return jsonify(
            data=[pInfo5.timestamps, pInfo5.orderOfProcesses, pInfo5.processes_list]
        )
    elif main_algorithm == "SRTF":
        pInfo6 = Process("SRTF")
        pInfo6.processes_list = processes_list
        pInfo6.multi_check = pInfo6.prio_check = False
        pInfo6.trimProcessList()
        print("\n\nSRTF:")
        SRTF(pInfo6)
        return jsonify(
            data=[pInfo6.timestamps, pInfo6.orderOfProcesses, pInfo6.processes_list]
        )
    elif main_algorithm == "MLQ":
        pInfo7 = Process("MLQ", *(mlq_algorithms))
        # pInfo7 = Process("PriorityNP", "SRTF")
        pInfo7.processes_list = processes_list
        pInfo7.trimProcessList()
        print(f"\n\nMLQ (Algorithms: {pInfo7.algorithms}):")
        MLQ(pInfo7)
        return jsonify(
            data=[pInfo7.timestamps, pInfo7.orderOfProcesses, pInfo7.processes_list]
        )
    elif main_algorithm == "MLFQ":
        if mlfq_algorithm == "MLQ":
            pInfo8 = Process("MLFQ", *mlq_algorithms)
        else:
            pInfo8 = Process("MLFQ", mlfq_algorithm)
        pInfo8.processes_list = processes_list
        pInfo8.QT = int(quantum_time) if quantum_time else None
        pInfo8.mlfq_qt = mlfq_qt
        pInfo8.mlfq_levels = len(mlfq_qt) + 1
        # print(pInfo8.processes_list)
        pInfo8.trimProcessList()
        print("\n\nMLFQ:")
        MLFQ(pInfo8)
        return (
            jsonify(
                data=[
                    pInfo8.timestamps,
                    pInfo8.orderOfProcesses,
                    pInfo8.processes_list,
                    pInfo8.mlfq_timestamps,
                    pInfo8.mlfq_orderOfProcesses,
                ]
            ),
            200,
        )


@app.route("/sendInputPageReplacement", methods=["POST"])
def handle_user_input_page_replacement():
    inputData = request.get_json()
    pageReplacementAlgorithm = inputData.get("pageReplacementAlgorithm")
    pageReferences = inputData.get("pageReferences")
    numberOfFrames = inputData.get("numberOfFrames")

    returnedData = PageReplacement(
        pageReplacementAlgorithm, pageReferences, numberOfFrames
    )

    return jsonify(returnedData)

    # return jsonify(inputData, framesSimulated, results)


@app.route("/sendInputCryptography", methods=["POST"])
def handle_user_input_cryptography():
    inputData = request.get_json()
    action = inputData.get("action")

    if action == "encrypt":
        fileToEncrypt = inputData.get("fileToEncrypt")
        fileToEncryptContent = inputData.get("fileToEncryptContent")
        keywordEncrypt = inputData.get("keywordEncrypt")

        returnedData = encrypt_my_algo(
            fileToEncryptContent, keywordEncrypt, fileToEncrypt
        )

        return jsonify(returnedData)

    elif action == "decrypt":
        fileToDecrypt = inputData.get("fileToDecrypt")
        fileToDecryptContent = inputData.get("fileToDecryptContent")
        privateKeyDecrypt = inputData.get("privateKeyDecrypt")
        modDecrypt = inputData.get("modDecrypt")
        keywordDecrypt = inputData.get("keywordDecrypt")
        otpDecrypt = inputData.get("otpDecrypt")

        returnedData = decrypt_my_algo(
            fileToDecryptContent,
            privateKeyDecrypt,
            modDecrypt,
            keywordDecrypt,
            otpDecrypt,
            fileToDecrypt,
        )

        return jsonify(returnedData)


@app.route("/sendInputDiskScheduling", methods=["POST"])
def handle_user_input_disk_scheduling():
    inputData = request.get_json()
    outputData = DiskScheduling(inputData)

    return outputData


# if __name__ == "__main__":
#     app.run(debug=False, host="0.0.0.0")
