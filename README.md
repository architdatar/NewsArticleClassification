# NewsArticleClassification
Classifying news articles based on their features. <br>
Group members: <br>
Yue Li <br>
Archit Datar <br>
Lauren Contard <br>
Haihang Wu <br>
Bobby Lumpkin <br>

Feb 25, 2021 <br>

1.	Intro about the project <br>
	a.	News articles from 10 mainstream media <br>
	b.	Covering how the White House delivers messages about COVID-19. <br>
	c.	Key words search (“white house/trump/pence” & “covid/coranavirus”) <br>
	d.	Drawback of the key words search method: we cannot get rid of some articles that are not about White House briefings.<br>
		i.	E.g. “WHO held a conference criticizing White House’s responses to COVID” <br>
	e.	“related” <br>
		i.	0-- the news articles are NOT related to White House briefings about COVID-19. For example, WHO held conferences in which they mentioned the White House and COVID. US governors held conferences in which they mentioned Trump. <br>
		ii.	1-- the news articles are related to White House briefings about COVID-19. As long as the news articles mentioned White House briefings/conferences about COVID-19, they should be counted as 1. For example, Dr. Fauci will attend the White House briefing. <br> 
2.	Dataset <br>
	a.	Training/test dataset (n=1345) <br>
	b.	Raw dataset (N=8045) <br>
3.	For the Exploratory Data Analysis assignment <br>
	a.	text-preprocessing. That is, tokenize the titles into words/features so that machine learning models could use for further analysis. (Yue: by Thursday/Friday early morning) <br>
	b.	Everything before plots (Bobby: by Friday night/Saturday early morning) <br>
	c.	Plots (Haihang: by Saturday night/Sunday morning) <br>
	d.	PCA (Archit: by Sunday morning/Sunday afternoon) <br>
	e.	Report (Lauren: by Sunday night) <br>

