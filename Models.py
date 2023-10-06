
import pandas as pd
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import MultinomialNB
import pickle


class AssistantModel:
    
    def Command(self,input):
        with open('AssistantModel.pkl', 'rb') as file:
            with open('Vectorizer.pkl','rb') as vectorizerfile:
                vectorizer = pickle.load(vectorizerfile)
                AssistantModel = pickle.load(file)
                user_input_vector = vectorizer.transform([input])
                predicted_action = AssistantModel.predict(user_input_vector)
                from sklearn.metrics import accuracy_score

                # True labels (ground truth)
                df = pd.read_excel('Assistant.xlsx')
                true_labels =  df['task']  # Replace with your actual true labels

                # Predicted labels from the model
                predicted_labels =  predicted_action# Replace with your predicted labels

                # Calculate accuracy
                # accuracy = accuracy_score(true_labels, predicted_labels)
                # print('Accuracy is ',accuracy)
                return "".join(predicted_action)
                
    def Train(self):
        print('Start Training')
        # with open('data.txt','r') as data:
        #     data = ast.literal_eval(data.read())
        #     df = pd.DataFrame(data)
        df = pd.read_excel('Assistant.xlsx')
        # Text vectorization using CountVectorizer
        print('Total Rows : ',len(df))
        vectorizer = CountVectorizer()
        X = vectorizer.fit_transform(df['command'])
        y = df['task']
        # Split the dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        # Train a Random Forest Classifier
        classifier = MultinomialNB()
        classifier.fit(X_train, y_train)
        
        with open('AssistantModel.pkl', 'wb') as file:
            pickle.dump(classifier, file)
            
        with open('Vectorizer.pkl', 'wb') as file:
            pickle.dump(vectorizer, file)
            
        print('Training completed')
        
 
            

    def updateData(self,command, task):
        print(command, task)
        new_row = {
            'command': command,
            'task':task
        }
        # with open('Assistant.xlsx','wb') as file:
        new_row_df = pd.DataFrame(new_row, index=[0])
        path = 'Assistant.xlsx'
        df = pd.read_excel(path)
        df = pd.concat([df, new_row_df], ignore_index=True)
        df.to_excel('Assistant.xlsx', index=False)

        # updated_data = ''
        # filename = 'data.txt'
        # with open(filename,'r') as dataset:
        #     content = dataset.read()
        #     data = ast.literal_eval(content)
        #     com = list(data['command'])
        #     label = list(data['task'])
        #     com.append(command)
        #     label.append(task)
        #     data['command'] = com
        #     data['task'] = label
        #     updated_data = repr(data)
            
        # with open(filename,'w') as file:
        #     file.write(updated_data)
        return 'updated'
    
# obj = AssistantModel()
# obj.Train()
    
