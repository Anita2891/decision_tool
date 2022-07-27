
import pandas as pd
import jinja2
from sklearn.preprocessing import MinMaxScaler
import util
import json
import multi_objective as moo

dataset={'region':{'NL':1,'DE': 2,'FR':3,'GB': 4},
        'feed':{'poultry':0,'milling':1,'fruit':2,'plant':3,'grain':4},
        'insect':{'house_cricket':0,'house_fly':1,'black_soldier_fly':2,'mealworm':3},
        'scaling':{'small':1,'medium':2,'large':3,'very_large':4}}

newset={'region':{1:'Netherland',2:'Germany',3:'France',4:'United Kingdom'},
        'feed':{0:'Poultry feed',1:'Milling-by-products',2:'Fruit and vegetables',3:'Plant residues',4:'Brewer spend grain'},
        'insect':{0:'House cricket',1:'House fly',2:'Black soldier fly',3:'Mealworm'},
        'scaling':{1:'Small (25 000-75 000 tons)',2:'Medium (75 000-125 000 tons)',3:'Large (125 000-175 000 tons)',4:'Very large (175 000-250 000 tons)'},
        'House cricket':'https://t3.ftcdn.net/jpg/00/66/02/60/240_F_66026002_hdD5sJsjy5heDzSHYwj9HgzdAxx0NT4u.jpg',
        'House fly':'https://previews.123rf.com/images/alekss/alekss1608/alekss160800540/62161524-a-macro-shot-of-fly-on-a-white-background-live-house-fly-insect-close-up.jpg',
        'Black soldier fly':'https://www.insectrearing.com/wp-content/uploads/2019/06/BSL_cover.png',
        'Mealworm':'https://media.istockphoto.com/photos/mealworms-tenebrio-molitor-darkling-beetle-larvae-on-white-background-picture-id177551209?k=20&m=177551209&s=612x612&w=0&h=Jx89x35xXXQQjrunKHty91thvMDR2CbEX4NmmB6yDlU=',
        'insectsImage':'https://media.springernature.com/lw685/springer-static/image/art%3A10.1186%2Fs13002-018-0258-z/MediaObjects/13002_2018_258_Fig2_HTML.png'}

#class for model logic
class Model:

    def __init__(self):
        pass

    # details of scenarios
    def getDetails(self):
        dfAll = pd.read_csv ('pareto-front_2.csv')
        dataFrame= dfAll[['SC','AIF', 'Economic_Impact','Environmental_Impact', 'Social_Impact','F0','F1','F2','F3','F4','I0','I1','I2','I3']]
        dataFrame.rename(columns = {'SC':'Scaling','AIF':'Amount of feed','F0':'Poultry feed','F1':'Milling-by-products','F2':'Fruits and vegetables','F3':'Plant residues',
                            'F4':'Brewery grains','I0':'House cricket','I1':'House fly','I2':'Black soldier fly','I3':'Mealworm'}, inplace = True)
        df = dataFrame.loc[:, ['Amount of feed', 'Economic_Impact','Environmental_Impact', 'Social_Impact']]
        scaler = MinMaxScaler() 
        scaled_values = scaler.fit_transform(df) 
        df.loc[:,:] = scaled_values
        utils= util.Util()
        styler = dataFrame.style.applymap(utils.colorNegativeRed)
        # Template handling
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath='templates'))
        template = env.get_template('details.html')
        html = template.render(my_table=styler.render())
        # Plot
        ax = df.plot.bar()
        fig = ax.get_figure()
        fig.savefig('static/plot.svg')
        # Write the HTML file
        with open('templates/report.html', 'w') as f:
            f.write(html)

        return True

    def getOptionsArray(self,optionString):
        try:
            utilObj=util.Util.convertStringArray(optionString)
            return utilObj
        except Exception as err:
            return err


    def getJsonForMOO(self, result):
        option=result['options']
        optionArr=self.getOptionsArray(option)
        objectives= result['objectives']
        feedArray=[0,0,0,0,0]
        insectArray=[0,0,0,0]
        regionArray=[]
        scalingArray=[]
        objectivesArray=[0,0,0]
        if 'feed' in optionArr.keys():
            feedArray[int(dataset['feed'][optionArr['feed']])]=1
        else:
            feedArray=[1,0,0,0,0]
        if 'insect' in optionArr.keys():
            insectArray[int(dataset['insect'][optionArr['insect']])]=1
        else:
            insectArray=[1,0,0,0]
        if 'region' in optionArr.keys():
            regionArray.append(int(dataset['region'][optionArr['region']]))
        else:
            regionArray=[2]
        if 'scales' in optionArr.keys():
            scalingArray.append(int(dataset['scaling'][optionArr['scales']]))
        else:
            scalingArray=[1]
        if objectives:
            optjectivesNew= objectives.replace(" ","").split(',')
            for data in optjectivesNew:
                objectivesArray[int(data)-1]=1
        else:
            objectivesArray=[1,1,1]
        dictToEnter= {'feed':feedArray,'insect':insectArray,'region':regionArray,'objectives':objectivesArray,'scaling':scalingArray}
        data1= json.dumps(dictToEnter)
        return json.loads(data1)
        
    def getScenarios(self,input):
        inputJson= self.getJsonForMOO(input)
        scenarioData=moo.main(inputJson)
        return scenarioData


    def reformatOut(self,inputDict):
        formattedData={}
        insect =[]
        feed =[]
        insectSet={}
        feedSet ={}
        insectImage={}
        for j in range(0,5):
            if inputDict["I0"][j]==1:
                insect.append('House cricket')
            if inputDict['I1'][j]==1:
                insect.append('House fly')
            if inputDict['I2'][j]==1:
                insect.append('Black soldier fly')
            if inputDict['I3'][j]==1:
                insect.append('Mealworm')

            if inputDict['I0'][j]==1:
                feed.append('Poultry feed')
            if inputDict['I1'][j]==1:
                feed.append('Milling-by-products')
            if inputDict['I2'][j]==1:
                feed.append('Fruits and vegetables')
            if inputDict['I3'][j]==1:
                feed.append('Plant residues')
            if inputDict['I0'][j]==1:
                feed.append('Brewers spend grain')
            if len(insect)==1:
                insectImage[j]=newset[insect[0]]
            else:
                insectImage[j]="https://media.springernature.com/lw685/springer-static/image/art%3A10.1186%2Fs13002-018-0258-z/MediaObjects/13002_2018_258_Fig2_HTML.png"

            insectSet[j]=" , ".join(str(x) for x in insect)
            feedSet[j]=" , ".join(str(x) for x in feed)
            description=[0,0,0,0,0]
        for i in range(0,5):
            text=''
            if feedSet[i]!='':
                text=text+'Feed types: '+feedSet[i]
            if insectSet[i]!='':
                text=text+'Insect types: '+insectSet[i]
            description[i]= text
            formattedData[i]={'scaling':newset['scaling'][inputDict['SC'][i]],'AIF':round(inputDict['AIF'][i],2),'Economic_Impact':round(inputDict['Economic_Impact'][i],2),'Environmental_Impact':round(inputDict['Environmental_Impact'][i],2), 'Social_Impact':round(inputDict['Social_Impact'][i],2),
                                'insect':insectSet[i],'feed':feedSet[i],'image':insectImage[i],'description':description[i]}
        return formattedData

