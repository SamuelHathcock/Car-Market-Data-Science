

# source = requests.get(self.url, headers=self.headers)
# soup = BeautifulSoup(source.text, 'html.parser')
# links = soup.findAll('a', class_='result-image gallery')

#Filtering a elements for the link text itself, which is under 'href'
# for i in range(len(links)):
#     links[i] = links[i]['href']

searchIndex = 0

mainURL = ["hahaha/", '0', '/lololol']

searchIndex += 120

mainURL[1] = str(searchIndex)

print(''.join(mainURL))