from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pycountry
import re
import json
import requests

QS = open("QS.txt", "r")
qs = QS.read().split('Q')
qs.append("covid cases")
qs.append("corona cases")
qs.append("corona patients")
qs.append("covid patients")
qs.append("coronavirus cases")
qs.append("coronavirus patients")

ANS = open("ANS.txt", "r")
ANS = ANS.read().split('X')
ANS.append('stat')
ANS.append('stat')
ANS.append('stat')
ANS.append('stat')
ANS.append('stat')
ANS.append('stat')

stopWords = set(" the a an and are - is how what when do does you I where ".split())
questions = []
for str in qs:
    s_list = [word for word in str.split() if word not in stopWords]
    str_ = ' '.join(s_list)
    questions.append(str_)

while (True):
    userInput = input("What do you want to ask me ? : \n")
    userInput = userInput.lower()

    vector = TfidfVectorizer(ngram_range=(1, 3))
    vector.fit(questions)

    vectorArray = vector.transform(questions).toarray()

    cosineSimStringCases = cosine_similarity(vectorArray)

    inputVector = vector.transform([userInput])
    inputVector.toarray()

    similarityValue = cosine_similarity(inputVector, vectorArray)

    if max(similarityValue[0]) < 0.1:
        print('Sorry, we don\'t know the answer to that question')
        continue
    indexOfMaxSimilarity = np.argmax(similarityValue)
    if ANS[indexOfMaxSimilarity] != 'stat':
        print(ANS[indexOfMaxSimilarity])
    else:
        cList = pycountry.countries
        countryList = []
        for count in cList:
            countryName = count.name
            countryName = countryName.lower()
            countryName = re.sub('\(', '', countryName)
            countryName = re.sub('\)', '', countryName)
            countryList.append(countryName)
        countryList.append("united states of america")

        country = "Global"
        found = False
        apiResponse = requests.get('https://api.covid19api.com/summary')
        list = userInput.split(' ')

        for i in countryList:
            if i in userInput:
                country = i
                found = True

        error = False
        try:
            responseJSON = json.loads(apiResponse.text)
        except:
            print("server not responding please input again")
            error = True

        if error:
            continue
        else:
            if found:
                globalStats = responseJSON['Countries']
                for i in range(0, len(globalStats)):
                    temp = globalStats[i]['Country'].lower()
                    if temp == country:
                        print(country.upper())
                        print('New Confirmed', globalStats[i]['NewConfirmed'])
                        print('Total Confirmed', globalStats[i]['TotalConfirmed'])
                        print('New Deaths', globalStats[i]['NewDeaths'])
                        print('Total Deaths', globalStats[i]['TotalDeaths'])
                        print('New Recovered', globalStats[i]['NewRecovered'])
                        print('Total Recovered', globalStats[i]['TotalRecovered'])

            else:
                globalStats = responseJSON['Global']
                print(country.upper())
                print('New Confirmed', globalStats['NewConfirmed'])
                print('Total Confirmed', globalStats['TotalConfirmed'])
                print('New Deaths', globalStats['NewDeaths'])
                print('Total Deaths', globalStats['TotalDeaths'])
                print('New Recovered', globalStats['NewRecovered'])
                print('Total Recovered', globalStats['TotalRecovered'])