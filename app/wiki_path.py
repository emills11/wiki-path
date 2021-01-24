import random
from collections import defaultdict
from typing import List
import wikipedia

class WikiPath:

    # Initialize class with page to start at, and the target page to search for
    def __init__(self, start: str, target: str):
        self.startPage = start
        self.targetPage = target

        self.sourceQueue = list()
        self.targetQueue = list()

        self.sourceVisited = defaultdict()
        self.targetVisited = defaultdict()

        self.sourceParent = defaultdict()
        self.targetParent = defaultdict()


    # Returns shuffled list of each link to other wiki pages from a given page
    def generateShuffledPageLinks(self, page: str) -> List[str]:

        wikipedia.set_rate_limiting(True)
        try:
            wikiPage = wikipedia.WikipediaPage(title=page)
        except wikipedia.PageError:
            return "PageError"
        
        allLinks = [x for x in wikiPage.links if "(identifier)" not in x]
        random.shuffle(allLinks)

        return allLinks[0:25]


    # Algorithm for finding path between pages
    # Does a single iteration of BFS
    def findPathBFS(self, direction="forward"):
        if direction == "forward":
            current = self.sourceQueue.pop(0)
            connectedLinks = self.generateShuffledPageLinks(current)

            if connectedLinks == "PageError":
                self.sourceQueue.clear()
                return

            for link in connectedLinks:
                if link not in self.sourceVisited:
                    self.sourceQueue.append(link)
                    self.sourceVisited[link] = True
                    self.sourceParent[link] = current
        else:
            current = self.targetQueue.pop(0)
            connectedLinks = self.generateShuffledPageLinks(current)

            if connectedLinks == "PageError":
                self.targetQueue.clear()
                return

            for link in connectedLinks:
                if (link not in self.targetVisited):
                    self.targetQueue.append(link)
                    self.targetVisited[link] = True
                    self.targetParent[link] = current

    # Checks if there are any intersects between the two searches
    def isPathIntersect(self) -> str:
        for link in self.targetQueue:
            if link in self.sourceVisited:
                return link
        
        return "No intersections"

    # Once an intersect has been found, generates a list of page strings to form a path
    def getPath(self, intersect: str) -> List[str]:
        path = list()
        path.append(intersect)
        current = intersect

        while current != self.startPage:
            path.append(self.sourceParent[current])
            current = self.sourceParent[current]

        path = path[::-1]
        current = intersect

        while current != self.targetPage:
            path.append(self.targetParent[current])
            current = self.targetParent[current]

        return path
        

    # Uses a bidirectional graph search algorithm to find a path between two Wikipedia pages
    # A BFS is started from both the beginning page, and the target page
    def findPathBidirectional(self):
        self.sourceQueue.append(self.startPage)
        self.sourceVisited[self.startPage] = True
        self.sourceParent[self.startPage] = -1

        self.targetQueue.append(self.targetPage)
        self.targetVisited[self.targetPage] = True
        self.targetParent[self.targetPage] = -1

        while self.sourceQueue and self.targetQueue:
            self.findPathBFS(direction="forward")
            
            self.findPathBFS(direction="backward")

            intersectingLink = self.isPathIntersect()

            if intersectingLink != "No intersections":
                return self.getPath(intersectingLink)
        
        return None