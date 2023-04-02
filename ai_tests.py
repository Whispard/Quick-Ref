testPdfs = {"habits": r"C:\Users\Jay\Downloads\Atomic habits ( PDFDrive ).pdf",
            "smart": r"D:\Books\David McRaney\You Are Not So Smart_ Why You Have (495)\You Are Not So Smart_ Why You H - David McRaney.pdf",
            "lect-1-2": r"CS302-Lect1-2-10Jan2023.pdf",
            "lect-3": r"CS302-Lect3-19Jan2023.pdf",
            "lect-4": r"CS302-Lect4-3Feb.pdf",
            }

data = {}
lastOpenPdf = None


def add(prompt,  pageNo, pdfName=""):
    global lastOpenPdf
    if lastOpenPdf != None and pdfName == "":
        data[prompt] = f"page - {pageNo} : {lastOpenPdf}"
    else:
        data[prompt] = f"page - {pageNo} : {testPdfs[pdfName]}"
        lastOpenPdf = testPdfs[pdfName]


# Less frequency words based tests
# add("PLATEAU OF LATENT POTENTIAL", "habits", 22)
# add("Pregame jitters",  108)
# add("addition by subtraction",  123)
# add("Two-Minute Rule",  127)
# add("Bryan Harris",, 162)
# add("explore/exploittrade-off.",  172)
#
# add("RKFBIIRSCBSUSSR",  17)
# add("Confabulation",  22)
# add("Ramachandran",  26)
# add("Family Guy",  42)

add("Die Hard 4",16,"lect-1-2")
add("Stuxnet", 18)
add("Regin",19)
add("Colonial Pipeline",23)

add("polyalphabetic",18,"lect-3")
add("Rail fence",19)
add("Polygram substitution",31)
add("Mathematician Lester Hill",37)
add("Vigenère table",44)
add("OTP - Vernam",50)

add("Jefferson Cylinder",5,"lect-4")
add("Enigma and M209 Cipher",10)
add("Phishing Attacks",34)
add("Quid pro quo",42)
add("Watering Hole",44)


# Exact sentence based
add("It was tailored as a platform for attacking modern SCADA and PLC systems",18,"lect-1-2")
add("Through possession of the private key of the ransom account, the FBI was able to retrieve the Bitcoin, though it did not disclose how it obtained the private key",25)
add("new tactics to spread their message of resistance in public spaces",29)
add("Its focus is to optimize operations--particularly the automation of processes and maintenance.",37)

add("Its focus is to optimize operations--particularly the automation of processes and maintenance",9,"lect-3")
add(" A mnemonic aid (a meaningful keyphrase) may be used to easily remember the 5x5 square",32)
add("polygram substitution ciphers (Playfair, Hill) are linear transformation, and fall under known-plaintext attack",41)
add("The cipher text is at the intersection of the row labeled key letter “k” and the column labeled text letter “p”.",44)

add("The cipher key is defined by the fixed wheel wirings and initial rotor positions",8,"lect-4")
add("It doesn’t appear to be anything other than what it is eg. A picture or music file",21)
add("Exploit the victim once trust and a weakness are established to advance the attack.",30)

# Similar sentence based
#add("")



def run_tests(collection):
    truths = 0
    corrects = 0
    total = len(data)
    for prompt, answer in data.items():
        results = collection.query(
            query_texts=[prompt],
            n_results=2
        )

        if data[prompt] in results['ids'][0]:
            corrects +=1
            if data[prompt] == results['ids'][0][0]:
                truths +=1
            print(prompt, results['ids'][0])
        else:
            print("FAILED: ",prompt, results['ids'][0])
    print(f"Truths: {truths} , Correct: {corrects}/{total} ({corrects/total*100:.2f}%)")
