import sqlite3
import uuid

import numpy as np
import openai
from openai.embeddings_utils import get_embedding


class LoreStore():
    def __init__(self, filename=None):

        self.conn = sqlite3.connect(filename)
        self.conn.execute("CREATE TABLE IF NOT EXISTS location_lore (key text unique, lore text, themes text, location text, region text, embedding text)")
        self.conn.execute("CREATE TABLE IF NOT EXISTS region_lore (key text unique, lore text, themes text, biome text, region text, embedding text)")
        self.conn.execute("CREATE TABLE IF NOT EXISTS region_edges (key text unique, origin text, dest text)")


    def close(self):
        self.conn.commit()
        self.conn.close()

    def __len__(self):
        rows = self.conn.execute('SELECT COUNT(*) FROM kv').fetchone()[0]
        return rows if rows is not None else 0



    def updateLocationEmbedding(self, key, engine="text-search-curie-doc-001"):
        cursor = self.conn.cursor()
        sql = '''SELECT lore, themes from location_lore where key=? '''

        #try:
        result = cursor.execute(sql, (key,)).fetchone()
        embedding = get_embedding(engine=engine, text=("{lore}, {themes}").format(lore=result[0], themes=result[1]))
        sql = '''update location_lore set embedding = ? where key = ?'''
        cursor.execute(sql, (str(embedding), key))

    def updateRegionEmbedding(self, key, engine="text-search-curie-doc-001"):
        cursor = self.conn.cursor()
        sql = '''SELECT lore, themes, biome from region_lore where key=? '''

        result = cursor.execute(sql, (key,)).fetchone()
        embedding = get_embedding(engine=engine, text=("{lore}, {themes}, {biome}").format(lore=result[0], themes=result[1], biome=result[2]))
        sql = '''update region_lore set embedding = ? where key = ?'''
        cursor.execute(sql, (str(embedding), key))


    def updateAllEmbeddings(self, engine="text-search-curie-doc-001"):
        cursor = self.conn.cursor()
        cursor.execute('SELECT key FROM location_lore')
        for row in cursor:
            self.updateLocationEmbedding(row[0], engine)

    def writeLocationLore(self, lore, themes, location, region):
        key = str(uuid.uuid1())
        cursor = self.conn.cursor()
        sql = '''INSERT OR REPLACE INTO location_lore (key, lore, themes, location, region ) VALUES (?, ?, ?, ?, ?)'''
        cursor.execute(sql, (key, lore, themes, location, region))
        self.updateLocationEmbedding(key)

    def writeRegionLore(self, lore, region, themes, biome):
        key = str(uuid.uuid1())
        cursor = self.conn.cursor()
        sql = '''INSERT OR REPLACE INTO region_lore (key, lore, themes, region, biome ) VALUES (?, ?, ?, ?, ?)'''
        cursor.execute(sql, (key, lore, themes, region, biome))
        self.updateRegionEmbedding(key)

    def most_similar(self, themes, location, region, engine="text-search-curie-query-001"):
        bestScore = 0
        query = "{location}, {region}, {themes}".format(location=location, themes=themes, region=region)
        embedding = get_embedding(text=query, engine=engine)
        cursor = self.conn.cursor()
        sql = ('''SELECT lore, embedding FROM location_lore where region=?''')
        cursor.execute(sql, (region,))
        best_score = 0
        best_match = ""
        scores = list()
        lore = list()
        for row in cursor:
            val = str(row[1])
            e = eval(val)
            match = np.dot(e, embedding)
            scores.append(match)
            lore.append(row[0])
        return sorted(zip(scores, lore), reverse=True)[:3]

    def knownRegions(self):
        sql = ('''SELECT distinct region FROM region_lore''')
        cursor = self.conn.cursor()
        cursor.execute(sql)
        return [i[0] for i in cursor.fetchall()]

    def knownLocations(self, region):
        sql = ('''SELECT distinct location FROM location_lore where region=?''')
        cursor = self.conn.cursor()
        cursor.execute(sql,(region,))
        return [i[0] for i in cursor.fetchall()]


    def readLore(self, key):
        cursor = self.conn.cursor()
        sql = '''SELECT lore from location_lore where key=? '''
        try:
            result = cursor.execute(sql, (key,))
            return result.fetchone()[0]
        except:
            return ""


    def regionEdges(self, region):
        cursor = self.conn.cursor()
        sql = '''SELECT dest from region_edges where orgigin=?'''
        result = cursor.execute(sql, (region,))
    def readLoreForLocation(self, region, location):
        cursor = self.conn.cursor()
        sql = '''SELECT lore from location_lore where region=? and location=? '''
        try:
            result = cursor.execute(sql, (region, location,))
            return result.fetchone()[0]
        except:
            return "Lore Missing"

    def readSummary(self, key):
        cursor = self.conn.cursor()
        sql = '''SELECT summary from location_lore where key=? '''
        try:
            result = cursor.execute(sql, (key,)).fetchone()
            return str(result)
        except:
            return ""

    def region_summary(self, region, themes, location):
        related = self.most_similar(region=region, themes=themes, location=location)
        prompt = ""
        print("Most relevant lore:")
        if (len(related) > 0):
            prompt = ("Summarize the following lore about {region}:\n").format(region=region)
            for entry in related:
                lore = entry[1]
                print(lore)
                prompt += lore



        prompt += ("\"\nSummary:")
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=prompt,
            max_tokens=200,
            temperature=0
        )
        return response.choices[0].text.strip()






