from flask import Flask, render_template, request
import models
import json
import multi_objective as moo

app = Flask(__name__,template_folder='templates')

#all countries for which fair wage potential present
region={'Netherland':'NL','Germany':'DE','France':'FR','United Kingdom': 'GB'}

#feed for insects
feed= {'Poultry feed':'poultry','Milling-by-products':'milling','Fruits abd vegetables':'fruit','Plant residues':'plant','Brewers spent grains':'grain'}

#scaling of production (AIF amount per tons)
scaling= {'Small (25 000-75 000 tons)':'small','Medium (75 000-125 000 tons)':'medium','Large (125 000-175 000 tons)':'large','Very large (175 000-250 000 tons)':'very_large'}

#types of insects 
insects={'House cricket (Acheta domesticus)':'house_cricket','House fly (Musca domestica)':'house_fly','Black soldier fly (Hermentia illucens)':'black_soldier_fly','Yellow mealworm (Tenebrio molitor)':'mealworm'}

#objectives
objective={'Economic aspect':1,'Environmental aspect':2,'Social aspect':3,}


#example scenarios
example=[{
    'image':"https://t3.ftcdn.net/jpg/00/66/02/60/240_F_66026002_hdD5sJsjy5heDzSHYwj9HgzdAxx0NT4u.jpg",
    'emission':['2046.71 kgCO2','5.836 m2','614.45 MJ','1000 Euro'],
    'options':['House cricket','Poultry feed','Whole dead', 'Paperboard'],
    'description': 'House cricket feed on poultry feed and whole dead larvae as final product and paperboard as packaging'

},
{
    'image':"https://previews.123rf.com/images/alekss/alekss1608/alekss160800540/62161524-a-macro-shot-of-fly-on-a-white-background-live-house-fly-insect-close-up.jpg",
    'emission':['2044.71 kgCO2','5.836 m2','482.45 MJ','1891 Euro'],
    'options':['House fly','Fruits and vegetables','Alive dead', 'Paperboard'],
    'description': 'House fly feed on fruits and vegetable and whole alive larvae as final product and paperboard as packaging'

},
{
    'image':"https://www.insectrearing.com/wp-content/uploads/2019/06/BSL_cover.png",
    'emission':['1046.71 kgCO2','10.836 m2','640.45 MJ','800 Euro'],
    'options':['Black soldier fly','Plant residue','Whole dead', 'Kraft-paper'],
    'description': 'Black soldier fly feed on plant residues and whole dead larvae as final product and kraftpaper as packaging'

},
{
    'image':"https://media.istockphoto.com/photos/mealworms-tenebrio-molitor-darkling-beetle-larvae-on-white-background-picture-id177551209?k=20&m=177551209&s=612x612&w=0&h=Jx89x35xXXQQjrunKHty91thvMDR2CbEX4NmmB6yDlU=",
    'emission':['2046.71 kgCO2','5.836 m2','614.45 MJ','1000 Euro'],
    'options':['Mealworm','Poultry feed','Whole dead', 'Paperboard'],
    'description': 'House cricket feed on poultry feed and whole dead larvae as final product and paperboard as packaging'

}
]

#route for decision support page
@app.route("/",methods=['POST','GET'])
def index():
    if request.method=="POST":
        requestData=request.form.to_dict()
        modelObj= models.Model()
        data= modelObj.getScenarios(requestData)
        dataForm= modelObj.reformatOut(data)
        data1= json.dumps(dataForm)
        return json.loads(data1)
        
    else:
        defaultData={0: {'scaling': 'Very large (175 000-250 000 tons)', 'AIF': 204142.88, 'Economic_Impact': 424082473.83, 'Environmental_Impact': 608390.65, 'Social_Impact': 0.67, 'insect': 'Black soldier fly', 'feed': 'Fruits and vegetables','description':'Insect type: Black soldier fly & Feed: Fruits and vegetables', 'image': 'https://www.insectrearing.com/wp-content/uploads/2019/06/BSL_cover.png'},
         1: {'scaling': 'Small (25 000-75 000 tons)', 'AIF': 55306.46, 'Economic_Impact': 86897467.43, 'Environmental_Impact': 439534.4, 'Social_Impact': 1.0, 'insect': 'Black soldier fly , House cricket ', 'feed': 'Fruits and vegetables , Poultry feed , Fruits and vegetables , Brewers spend grain','description': 'Insect type: Black soldier fly , House cricket & Feed: Poultry feed  , Brewers spend grain','image': 'https://media.springernature.com/lw685/springer-static/image/art%3A10.1186%2Fs13002-018-0258-z/MediaObjects/13002_2018_258_Fig2_HTML.png'}, 
         2: {'scaling': 'Small (25 000-75 000 tons)', 'AIF': 55813.32, 'Economic_Impact': 102090962.13, 'Environmental_Impact': 443562.52, 'Social_Impact': 0.96, 'insect': 'Black soldier fly , House cricket , Black soldier fly , House cricket', 'feed': 'Fruits and vegetables , Poultry feed  , Brewers spend grain ','description': 'Insect type: Black soldier fly , House cricket & Feed: Poultry feed  , Brewers spend grain', 'image': 'https://media.springernature.com/lw685/springer-static/image/art%3A10.1186%2Fs13002-018-0258-z/MediaObjects/13002_2018_258_Fig2_HTML.png'},
        3: {'scaling': 'Very large (175 000-250 000 tons)', 'AIF': 200925.37, 'Economic_Impact': 337776577.39, 'Environmental_Impact': 598801.76, 'Social_Impact': 1.0, 'insect': 'Black soldier fly , House cricket , Black soldier fly , House cricket', 'feed': 'Fruits and vegetables , Poultry feed , Fruits and vegetables , Brewers spend grain , Poultry feed , Brewers spend grain','description': 'Insect type: Black soldier fly , House cricket & Feed: Poultry feed  , Plant residues' ,'image': 'https://media.springernature.com/lw685/springer-static/image/art%3A10.1186%2Fs13002-018-0258-z/MediaObjects/13002_2018_258_Fig2_HTML.png'},
         4: {'scaling': 'Very large (175 000-250 000 tons)', 'AIF': 204370.74, 'Economic_Impact': 337446700.77, 'Environmental_Impact': 609069.71, 'Social_Impact': 1.0, 'insect': 'Black soldier fly , House cricket , Black soldier fly , House cricket', 'feed': 'Fruits and vegetables , Poultry feed , Fruits and vegetables , Brewers spend grain , Poultry feed , Brewers spend grain','description': 'Insect type: Black soldier fly , House fly & Feed: Poultry feed  , Brewers spend grain', 'image': 'https://media.springernature.com/lw685/springer-static/image/art%3A10.1186%2Fs13002-018-0258-z/MediaObjects/13002_2018_258_Fig2_HTML.png'}}
        if defaultData:
            dataForm=defaultData
        else:
            defaultInput={"insect":[1,0,0,0],"feed":[1,0,0,0,0],"region":[2],"objectives":[1,1,1],"scaling":[1,2,3]}
            data1= json.dumps(defaultInput)
            inputString= json.loads(data1)
            modelObj= models.Model()
            data= moo.main(inputString)
            dataForm= modelObj.reformatOut(data)
        return render_template('decision_tool.html',regionInfo=region,scalingOptions=scaling,insectType=insects,objectives=objective,feedOptions=feed,example=dataForm)


@app.route("/details",methods=['POST','GET'])
def details():
    modelObj= models.Model()
    modelObj.getDetails()
    return render_template('report.html')

