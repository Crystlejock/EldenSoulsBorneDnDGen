import sqlite3
import uuid

import numpy as np
import openai
from openai.embeddings_utils import get_embedding
import graphviz


class LoreStore():
    def __init__(self, filename=None):

        self.conn = sqlite3.connect(filename)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS location_lore (key text unique, lore text, themes text, location text, region text, embedding text)")
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS region_lore (key text unique, lore text, themes text, biome text, region text, embedding text)")
        self.conn.execute("CREATE TABLE IF NOT EXISTS region_edges (key text unique, origin text, dest text)")
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS location_edges (key text unique, origin text, dest text, region text)")
        self.conn.commit()
        self.filename = filename
        self.name = filename[:-len(".db")]

    def expoertData(self):
        dot = graphviz.Digraph('regions', comment='Region Map')
        regions = self.knownRegions()
        done = set()
        for idx, region in enumerate(regions):
            data = self.readDataForRegion(region)
            dot.node(region, region + "\n Biome:" + data['biome'] + "\nThemes:" + data['themes'], href=region+"_map.html")
            done.add(region)
            for other in self.regionEdges(region):
                if other not in done:
                    dot.edge(region, other, dir='none')

        regions = self.knownRegions()
        for region in regions:
            region_data = self.readDataForRegion(region)
            c = graphviz.Digraph(region, comment=region + ' Map')
            c.attr(label=region)
            done = set()
            locations = self.knownLocations(region)
            for idx, location in enumerate(locations):
                data = self.readDataForLocation(region, location)
                c.node(location, location + "\nThemes:" + data['themes'], href=location+"_map.html")
                done.add(location)
                fl = open(self.name + "/" + location + "_map.html", "w")
                fl.write("<h1>{location}</h1>".format(location=location))
                fl.write("<div style=\"white-space: pre-wrap;\">{lore}</div>".format(lore=data['lore']))
                fl.close()
                for other in self.locationEdges(region=region, location=location):
                    if other not in done:
                        other_data = self.readDataForLocation(region=region, location=other)
                        c.edge(location, other, dir='none')
            c.format = 'png'
            c.render(directory=self.name)
            c.format = 'svg'
            c.render(directory=self.name)
            f = open(self.name + "/"+region+"_map.html", "w")
            f.write("<h1>{region}</h1>".format(region=region))
            f.write("<div style=\"white-space: pre-wrap;\">{lore}</div>".format(lore=region_data['lore']))
            f.write(
                "<object style=\"width:100%;height:100%\" data=\""+region+".gv.svg\" type=\"image/svg+xml\"><span>Your browser doesn't support SVG images</span></object>")

        dot.format = 'png'
        dot.render(directory=self.name)
        dot.format = 'svg'
        dot.render(directory=self.name)
        f = open(self.name+"/world_map.html", "w")
        f.write("<object style=\"width:100%;height:100%\" data=\"regions.gv.svg\" type=\"image/svg+xml\"><span>Your browser doesn't support SVG images</span></object>")




    def close(self):
        self.conn.commit()
        self.conn.close()

    def __len__(self):
        rows = self.conn.execute('SELECT COUNT(*) FROM kv').fetchone()[0]
        return rows if rows is not None else 0

    def updateLocationEmbedding(self, key, engine="text-search-curie-doc-001"):
        cursor = self.conn.cursor()
        sql = '''SELECT lore, themes from location_lore where key=? '''

        # try:
        result = cursor.execute(sql, (key,)).fetchone()
        embedding = get_embedding(engine=engine, text=("{lore}, {themes}").format(lore=result[0], themes=result[1]))
        sql = '''update location_lore set embedding = ? where key = ?'''
        cursor.execute(sql, (str(embedding), key))
        self.conn.commit()

    def updateRegionEmbedding(self, key, engine="text-search-curie-doc-001"):
        cursor = self.conn.cursor()
        sql = '''SELECT lore, themes, biome from region_lore where key=? '''

        result = cursor.execute(sql, (key,)).fetchone()
        embedding = get_embedding(engine=engine,
                                  text=("{lore}, {themes}, {biome}").format(lore=result[0], themes=result[1],
                                                                            biome=result[2]))
        sql = '''update region_lore set embedding = ? where key = ?'''
        cursor.execute(sql, (str(embedding), key))
        self.conn.commit()

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
        self.conn.commit()

    def writeRegionLore(self, lore, region, themes, biome):
        key = str(uuid.uuid1())
        cursor = self.conn.cursor()
        sql = '''INSERT OR REPLACE INTO region_lore (key, lore, themes, region, biome ) VALUES (?, ?, ?, ?, ?)'''
        cursor.execute(sql, (key, lore, themes, region, biome))
        self.conn.commit()
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
        cursor.execute(sql, (region,))
        data = cursor.fetchall()
        return [i[0] for i in data]

    def readLore(self, key):
        cursor = self.conn.cursor()
        sql = '''SELECT lore from location_lore where key=? '''
        try:
            result = cursor.execute(sql, (key,))
            return result.fetchone()[0]
        except:
            return ""

    def locationEdges(self, location, region):
        cursor = self.conn.cursor()
        sql = '''SELECT dest from location_edges where origin=? and region =?'''
        matched = []
        cursor.execute(sql, (location, region))
        for row in cursor:
            matched.append(row[0])
        return matched

    def removeLocationEdge(self, location, other, region):
        cursor = self.conn.cursor()
        sql = '''DELETE from location_edges where origin=? and dest=? and region=?'''
        cursor.execute(sql, (location, other, region))
        cursor.execute(sql, (other, location, region))
        self.conn.commit()

    def addLocationEdge(self, location, other, region):
        cursor = self.conn.cursor()
        sql = '''INSERT OR REPLACE INTO location_edges (origin, dest, region) VALUES (?,?,?)'''
        cursor.execute(sql, (location, other, region))
        cursor.execute(sql, (other, location, region))
        self.conn.commit()

    def regionEdges(self, region):
        cursor = self.conn.cursor()
        sql = '''SELECT dest from region_edges where origin=?'''
        matched = []
        cursor.execute(sql, (region,))
        for row in cursor:
            matched.append(row[0])
        return matched

    def removeRegionEdge(self, region, other):
        cursor = self.conn.cursor()
        sql = '''DELETE from region_edges where origin=? and dest=?'''
        cursor.execute(sql, (region, other))
        cursor.execute(sql, (other, region))
        self.conn.commit()

    def addRegionEdge(self, region, other):
        cursor = self.conn.cursor()
        sql = '''INSERT OR REPLACE INTO region_edges (origin, dest) VALUES (?,?)'''
        cursor.execute(sql, (region, other))
        cursor.execute(sql, (other, region))
        self.conn.commit()

    def readLoreForLocation(self, region, location):
        cursor = self.conn.cursor()
        sql = '''SELECT lore from location_lore where region=? and location=? '''
        try:
            result = cursor.execute(sql, (region, location,))
            return result.fetchone()[0]
        except:
            return "Lore Missing for Location"

    def readDataForLocation(self, region, location):
        cursor = self.conn.cursor()
        sql = '''SELECT lore, themes from location_lore where region=? and location=? '''
        try:
            cursor.execute(sql, (region, location,))
            return dict(cursor.fetchall()[0])
        except:
            return "Location Data Missing"

    def readDataForRegion(self, region):
        cursor = self.conn.cursor()
        sql = '''SELECT region, lore, biome, themes from region_lore where region=?'''
        try:
            cursor.execute(sql, (region,))
            return dict(cursor.fetchall()[0])
        except:
            return "Region Data Missing"

    def readSummary(self, key):
        cursor = self.conn.cursor()
        sql = '''SELECT summary from location_lore where key=? '''
        try:
            result = cursor.execute(sql, (key,)).fetchone()
            return str(result)
        except:
            return ""

    def summaryRegionAndConnected(self, region, location):
        connected = self.locationEdges(location, region)

        regionLore = self.readDataForRegion(region)['lore']
        prompt = ("Summarize the following lore about {region}:\n").format(region=region)
        prompt += regionLore
        if (len(connected) > 0):
            prompt += "Nearby to {location} can be found \n".format(location=location)
            for entry in connected:
                lore = self.readDataForLocation(region, entry)['lore']
                prompt += lore

        prompt += ("\"\nSummary:")
        print("========")
        print("Summary Prompt: " + prompt)
        print("======")
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=prompt,
            max_tokens=200,
            temperature=0
        )
        return response.choices[0].text.strip()

    def summaryConnectedRegions(self, region):
        connected = self.regionEdges(region)

        prompt = ("Summarize the following lore about regaion contected to {region}:\n").format(region=region)
        if (len(connected) > 0):
            prompt += "Nearby {region} can be found the following reagions: \n".format(region=region)
            for entry in connected:
                lore = self.readDataForRegion(entry)['lore']
                prompt += lore

        prompt += ("\"\nSummary:")
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=prompt,
            max_tokens=200,
            temperature=0
        )
        return response.choices[0].text.strip()

    def summaryFromSimilar(self, region, themes, location):
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
