import csv


def get_moods():

    # Open the TSV file
    data = []
    moods = []

    with open('mtg_jamendo/data/autotagging_moodtheme.tsv', newline='', encoding='utf-8') as tsvfile:
        # specify tab as the delimiter
        reader = csv.reader(tsvfile, delimiter='\t')

        data = list(reader)

        for row in data[1:]:  # loop through rows in data, skip 1st row containing headers

            moodThemeList = row[5:]  # get array of all moods/themes

            listOfMoodsText = "mood/theme--"
            for mood in moodThemeList:  # loop through each mood in moodThemeList and get the moods,
                temp = mood.split('-')

                listOfMoodsText = listOfMoodsText + temp[3] + ", "
                if temp[3] not in moods:  # temp[3] is the mood
                    moods.append(temp[3])

            listOfMoodsText = listOfMoodsText[:-2]  # delete the last ", "

            row[5] = listOfMoodsText

            del row[6:]

        with open('modified_autotagging_moodtheme.tsv', 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile, delimiter='\t')
            writer.writerows(data)

        return moods

moods = get_moods()
print(moods)