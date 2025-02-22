from datetime import datetime
from gluonts.mx import Trainer, DeepAREstimator, SimpleFeedForwardEstimator
from gluonts.mx.distribution import NegativeBinomialOutput

class Configuration:
    def __init__(self):
        self.train_start_time = datetime(1999,1,1,0,0,0)
        self.train_end_time = datetime(2016,9,30,23,0,0)
        self.test_end_time = datetime(2018,9,30,23,0,0)
        self.validation_end_time = datetime(2020, 9, 30, 23, 0, 0)
        # color palette we used for our visualizations
        self.colors = ["#003f5c", "#ff0033", "#47c9b8", "#F8D7DA", "#B7D1CD", "#F5B0CB", "#9FB1BC", "#FEECC2",
                       "#FFE5D9", "#A4C2E0", "#D9EAD3", "#C3E0E5", "#F5C9B0","#b3a2c7", "#e6a0c4","#9ac1c6",
                       "#d1bea8", "#f6b870", "#a5d3cd", "#c291a5","#fed98e", "#72c9c2", "#fca6a3", "#6db8ca", "#ffcf84",
                       "#a8c6d1", "#ffa85e", "#f6a6b2", "#89c2c9", "#a7d49b"]
        
        # parameters and estimator of the DeepAR model (note these may not be equal to the default parameters)
        self.parameters = {
            "freq" : "W-SUN",
            "context_length" : 4,   # in number of weeks
            "prediction_length" : 4,   # in number of weeks ->1 Week (104 Test Windows), 13W(8TW), 26W(4TW), 52W(2TW),... 
            "num_layers" : 2,
            "num_cells" : 32,
            "cell_type" : "lstm",
            "epochs" : 8,
            "learning_rate": 0.001,
            #"num_batches_per_epoch":50,
            "batch_size":32,
            "dropout_rate":0.1,
            "distr_output" : NegativeBinomialOutput(),
            "use_feat_dynamic_real" : False,
            "use_feat_static_real" : False,
            "use_feat_static_cat" : False,
            "cardinality" : None,
        }

        self.deeparestimator = DeepAREstimator(freq=self.parameters["freq"],
                        context_length=self.parameters["context_length"],
                        prediction_length=self.parameters["prediction_length"],
                        num_layers=self.parameters["num_layers"],
                        num_cells=self.parameters["num_cells"],
                        cell_type=self.parameters["cell_type"],
                        dropout_rate = self.parameters["dropout_rate"],
                        trainer=Trainer(epochs=self.parameters["epochs"],
                                       learning_rate=self.parameters["learning_rate"],
                                       #num_batches_per_epoch=self.parameters["num_batches_per_epoch"]
                                       ),
                        batch_size=self.parameters["batch_size"],
                        distr_output=self.parameters["distr_output"],
                        use_feat_static_real=self.parameters["use_feat_static_real"],
                        use_feat_static_cat=self.parameters["use_feat_static_cat"],
                        use_feat_dynamic_real=self.parameters["use_feat_dynamic_real"],
                        cardinality=self.parameters["cardinality"],
                        )
        
        # parameters and estimator of the FNN model (note these may not be equal to the default parameters)
        self.fnnparameters = {
            "context_length" : 4,   # in number of weeks
            "prediction_length" : 4,   # in number of weeks ->1 Week (104 Test Windows), 13W(8TW), 26W(4TW), 52W(2TW),... 
            "epochs" : 8,
            "distr_output" : NegativeBinomialOutput(),
            "num_hidden_dimensions":[10],
            "num_batches_per_epoch":50,
            "batch_normalization":False,
            "batch_size":32,
        }
        self.feedforwardestimator = SimpleFeedForwardEstimator(num_hidden_dimensions=self.fnnparameters["num_hidden_dimensions"],
                                                              prediction_length=self.fnnparameters["prediction_length"],
                                                              context_length=self.fnnparameters["context_length"],
                                                              distr_output=self.fnnparameters["distr_output"],
                                                              batch_size=self.fnnparameters["batch_size"],
                                                              batch_normalization=self.fnnparameters["batch_normalization"],
                                                              trainer=Trainer(epochs=self.fnnparameters["epochs"],
                                                                              #learning_rate=self.parameters["learning_rate"],
                                                                              num_batches_per_epoch=self.fnnparameters["num_batches_per_epoch"],
                                                                             ),
                                                              )
        
        # the target column of the influenza dataset -> important for preprocessing
        self.target = "value"
        self.quantiles = [0.025, 0.1, 0.25, 0.5, 0.75, 0.9, 0.975]
        
                
        # number of forecasting windows we want to produce -> determined indirectly through the prediction_length
        self.windows = int(104 / self.parameters["prediction_length"])
        
        # handling of some LKs that were not matched correctly between different datasets (e.g. the Adjacency Dataset, the Influenza Dataset and the Influenza Dataset)
        self.specific_matches={'Altenkirchen (Westerwald)': ['LK Altenkirchen'],
                          'Amberg': ['SK Amberg'],
                          'Ansbach': ['LK Ansbach', 'SK Ansbach'],
                          'Aschaffenburg': ['LK Aschaffenburg', 'SK Aschaffenburg'],
                          'Augsburg': ['LK Augsburg', 'SK Augsburg'],
                          'Bamberg': ['LK Bamberg', 'SK Bamberg'],
                          'Bayreuth': ['SK Bayreuth', 'LK Bayreuth'],
                          'Brandenburg an der Havel': ['SK Brandenburg a.d.Havel'],
                          'Coburg': ['LK Coburg', 'SK Coburg'],
                          'Darmstadt': ['SK Darmstadt'],
                          'Dillingen a.d. Donau': ['LK Dillingen a.d.Donau'],
                          'Eifelkreis-Bitburg-Prüm': ['LK Bitburg-Prüm'],
                          'Eisenach': [],                # not available in the influenza location names
                          'Erlangen': ['SK Erlangen'],
                          'Flensburg': ['SK Flensburg'],
                          'Frankenthal (Pfalz)': ['SK Frankenthal'],
                          'Freiburg im Breisgau': ['SK Freiburg i.Breisgau'],
                          'Fürth': ['LK Fürth', 'SK Fürth'],
                          'Gera': ['SK Gera'],
                          'Halle (Saale)': ['SK Halle'],
                          'Heilbronn': ['LK Heilbronn', 'SK Heilbronn'],
                          'Hof': ['LK Hof', 'SK Hof'],
                          'Kaiserslautern': ['LK Kaiserslautern', 'SK Kaiserslautern'],
                          'Karlsruhe': ['LK Karlsruhe', 'SK Karlsruhe'],
                          'Kassel': ['LK Kassel', 'SK Kassel'],
                          'Kempten (Allgäu)': ['SK Kempten'],
                          'Koblenz': ['SK Koblenz'],
                          'Landau in der Pfalz': ['SK Landau i.d.Pfalz'],
                          'Landsberg am Lech': ['LK Landsberg a.Lech'],
                          'Landshut': ['LK Landshut', 'SK Landshut'],
                          'Leipzig': ['LK Leipzig', 'SK Leipzig'],
                          'Lindau (Bodensee)': ['LK Lindau'],
                          'Ludwigshafen am Rhein': ['SK Ludwigshafen'],
                          'Mainz': ['SK Mainz'],
                          'Mühldorf a. Inn': ['LK Mühldorf a.Inn'],
                          'Mülheim an der Ruhr': ['SK Mülheim a.d.Ruhr'],
                          'München': ['LK München', 'SK München'],
                          'Neumarkt i.d. OPf.': ['LK Neumarkt i.d.OPf.'],
                          'Neustadt a.d. Aisch-Bad Windsheim': ['LK Neustadt a.d.Aisch-Bad Windsheim'],
                          'Neustadt a.d. Waldnaab': ['LK Neustadt a.d.Waldnaab'],
                          'Neustadt an der Weinstraße': ['SK Neustadt a.d.Weinstraße'],
                          'Nürnberg': ['SK Nürnberg'], 
                          'Offenbach': ['LK Offenbach'], 
                          'Offenbach am Main': ['SK Offenbach'], 
                          'Oldenburg': ['LK Oldenburg'],
                          'Oldenburg (Oldenburg)': ['SK Oldenburg'],    
                          'Osnabrück': ['LK Osnabrück', 'SK Osnabrück'],
                          'Osterode am Harz': [],             # not available in the influenza location names
                          'Passau': ['LK Passau', 'SK Passau'],
                          'Pfaffenhofen a.d. Ilm': ['LK Pfaffenhofen a.d.Ilm'],
                          'Potsdam': ['SK Potsdam'],
                          'Regen': ['LK Regen'],
                          'Regensburg': ['LK Regensburg', 'SK Regensburg'],
                          'Rosenheim': ['LK Rosenheim', 'SK Rosenheim'],
                          'Rostock': ['LK Rostock', 'SK Rostock'],
                          'Schweinfurt': ['LK Schweinfurt', 'SK Schweinfurt'],
                          'St. Wendel': ['LK Sankt Wendel'],
                          'Straubing': ['SK Straubing'],
                          'Trier': ['SK Trier'],
                          'Ulm': ['SK Ulm'],
                          'Weiden i.d. OPf.': ['SK Weiden i.d.OPf.'], 
                          'Weimar': ['SK Weimar'],
                          'Worms': ['SK Worms'],
                          'Wunsiedel i. Fichtelgebirge': ['LK Wunsiedel i.Fichtelgebirge'],
                          'Würzburg': ['LK Würzburg', 'SK Würzburg']}
        
        # manually determined adjacency relations between each LK of Berlin to other LKs
        self.berlin_neighbors = {'SK Berlin Charlottenburg-Wilmersdorf':['SK Berlin Mitte', 'SK Berlin Reinickendorf','SK Berlin Spandau',
                                                                        'SK Berlin Steglitz-Zehlendorf','SK Berlin Tempelhof-Schöneberg'],
                                 'SK Berlin Friedrichshain-Kreuzberg':['SK Berlin Lichtenberg','SK Berlin Mitte','SK Berlin Neukölln',
                                                                      'SK Berlin Pankow','SK Berlin Tempelhof-Schöneberg',
                                                                      'SK Berlin Treptow-Köpenick'],
                                 'SK Berlin Lichtenberg':['SK Berlin Friedrichshain-Kreuzberg','SK Berlin Marzahn-Hellersdorf',
                                                         'SK Berlin Pankow', 'SK Berlin Treptow-Köpenick', 'LK Barnim'],
                                 'SK Berlin Marzahn-Hellersdorf':['SK Berlin Lichtenberg', 'SK Berlin Treptow-Köpenick',
                                                                 'LK Barnim', 'LK Märkisch-Oderland'],
                                 'SK Berlin Mitte':['SK Berlin Charlottenburg-Wilmersdorf','SK Berlin Friedrichshain-Kreuzberg',
                                                   'SK Berlin Pankow','SK Berlin Reinickendorf', 'SK Berlin Tempelhof-Schöneberg'],
                                 'SK Berlin Neukölln':['SK Berlin Friedrichshain-Kreuzberg', 'SK Berlin Tempelhof-Schöneberg',
                                                      'SK Berlin Treptow-Köpenick', 'LK Dahme-Spreewald'],
                                 'SK Berlin Pankow':['SK Berlin Friedrichshain-Kreuzberg','SK Berlin Lichtenberg','SK Berlin Mitte',
                                                    'SK Berlin Reinickendorf', 'LK Barnim', 'LK Oberhavel'],
                                 'SK Berlin Reinickendorf':['SK Berlin Charlottenburg-Wilmersdorf','SK Berlin Mitte','SK Berlin Pankow',
                                                           'SK Berlin Spandau', 'LK Oberhavel'],
                                 'SK Berlin Spandau':['SK Berlin Charlottenburg-Wilmersdorf','SK Berlin Reinickendorf',
                                                     'SK Berlin Steglitz-Zehlendorf', 'LK Oberhavel', 'LK Havelland', 'SK Potsdam'],
                                 'SK Berlin Steglitz-Zehlendorf':['SK Berlin Charlottenburg-Wilmersdorf', 'SK Berlin Spandau',
                                                                 'SK Berlin Tempelhof-Schöneberg', 'SK Potsdam', 'LK Potsdam-Mittelmark',
                                                                 'LK Teltow-Fläming'],
                                 'SK Berlin Tempelhof-Schöneberg':['SK Berlin Charlottenburg-Wilmersdorf','SK Berlin Friedrichshain-Kreuzberg',
                                                                  'SK Berlin Mitte','SK Berlin Neukölln','SK Berlin Steglitz-Zehlendorf',
                                                                  'LK Dahme-Spreewald', 'LK Teltow-Fläming'],
                                 'SK Berlin Treptow-Köpenick':['SK Berlin Friedrichshain-Kreuzberg','SK Berlin Lichtenberg',
                                                               'SK Berlin Marzahn-Hellersdorf','SK Berlin Neukölln', 'LK Märkisch-Oderland',
                                                              'LK Dahme-Spreewald', 'LK Oder-Spree'],
                                 'SK Potsdam': ['LK Havelland', 'LK Potsdam-Mittelmark', 'SK Berlin Spandau',
                                                'SK Berlin Steglitz-Zehlendorf'],
                                 'LK Barnim': ['LK Märkisch-Oderland', 'LK Oberhavel', 'LK Uckermark', 'SK Berlin Lichtenberg',
                                              'SK Berlin Marzahn-Hellersdorf', 'SK Berlin Pankow'],
                                 'LK Dahme-Spreewald': ['LK Elbe-Elster', 'LK Oberspreewald-Lausitz', 'LK Oder-Spree',
                                                        'LK Spree-Neiße', 'LK Teltow-Fläming', 'SK Berlin Treptow-Köpenick', 
                                                        'SK Berlin Tempelhof-Schöneberg', 'SK Berlin Neukölln'],
                                 'LK Havelland': ['SK Brandenburg a.d.Havel', 'SK Potsdam', 'LK Oberhavel', 'LK Ostprignitz-Ruppin',
                                                  'LK Potsdam-Mittelmark', 'LK Jerichower Land', 'LK Stendal', 'SK Berlin Spandau'],
                                 'LK Märkisch-Oderland': ['SK Frankfurt (Oder)', 'LK Barnim', 'LK Oder-Spree',
                                                         'SK Berlin Marzahn-Hellersdorf', 'SK Berlin Treptow-Köpenick'],
                                 'LK Oberhavel': ['LK Barnim', 'LK Havelland', 'LK Ostprignitz-Ruppin', 'LK Uckermark',
                                                  'LK Mecklenburgische Seenplatte', 'SK Berlin Pankow', 'SK Berlin Reinickendorf',
                                                  'SK Berlin Spandau'],
                                 'LK Oder-Spree': ['SK Frankfurt (Oder)', 'LK Dahme-Spreewald', 'LK Märkisch-Oderland', 'LK Spree-Neiße',
                                                  'SK Berlin Treptow-Köpenick'],
                                 'LK Potsdam-Mittelmark': ['SK Brandenburg a.d.Havel', 'SK Potsdam', 'LK Havelland', 'LK Teltow-Fläming',
                                                           'LK Anhalt-Bitterfeld', 'LK Wittenberg', 'LK Jerichower Land',
                                                           'SK Berlin Steglitz-Zehlendorf'],
                                 'LK Teltow-Fläming': ['LK Dahme-Spreewald', 'LK Elbe-Elster', 'LK Potsdam-Mittelmark', 'LK Wittenberg',
                                                      'SK Berlin Tempelhof-Schöneberg', 'SK Berlin Steglitz-Zehlendorf']}
