//
//  TriviaView.swift
//  triviapi
//
//  Created by Victoria Lucero on 11/11/22.
//

import SwiftUI

struct TriviaView: View {
    @EnvironmentObject var triviaManager: TriviaManager
    @State var showViewAprende: Bool = false
    @State var mensj : Mensaje?
    struct Mensaje : Codable{
        var msj : String = ""
    }

    // llamada a la api
    
    func mandarCali(){
        guard let url = URL(string: APIURL + "/user/setGrade") else{
            return
        }
        let body: [String:AnyHashable] = [
            "_id" : logedUser._id,
            "categorie": TriviaCategor,
            "grade":(Float(triviaManager.score) / Float(triviaManager.length)) * 100 // porcentaje
        ]
        var request = URLRequest(url:url)//lo convertimos en una request para poder poner que es post y un body
        request.httpMethod = "POST"//ponemos su metodo como post
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = try? JSONSerialization.data(withJSONObject: body, options: .fragmentsAllowed)//ponemos el body con los datos en el request
        let task = URLSession.shared.dataTask(with: request) {data, _, error in
            
            guard let data = data, error == nil else{
                return
            }
            do{
                // en este do intentaremos crear el mensaje
                let response = try JSONDecoder().decode(Mensaje.self, from: data)// tratamos de decodearlo en una estructura de tipo User
                
                if(response.msj == "Level UP"){
                    logedUser.lvl = logedUser.lvl + 1;
                    mensj?.msj = "Has subido de nivel a " + String(logedUser.lvl) + "!!!"
                }   
                mensj = response   
            }
            catch{
                print("ERROR")
            }

            
        }
        task.resume()
    }
    

    var body: some View {
        
        if triviaManager.reachedEnd{
            // aqui mandamos la calificación del usuario jaja
            
            VStack(spacing: 20){
                
                NavigationLink(destination: AprenderView().navigationBarBackButtonHidden(true), isActive: $showViewAprende){
                    Text("")
                }
                
                title(text:"Quizz")
                Text("Tu puntuación fue \(triviaManager.score) de \(triviaManager.length)")
                
                Text(mensj?.msj ?? "")

                Button{
                    Task.init{
                        showViewAprende = true
                    }
                } label: {
                    PrimaryButtom(text: "Terminar")
                }
            }
            .onAppear(){
                mandarCali()
            }
            .foregroundColor(Color("AccentColor"))
                .padding()
                .frame(maxWidth: .infinity, maxHeight: .infinity)
                .background(.white)
            

        }else{
            QuestionView()
                .environmentObject(triviaManager)
        }
       
    }
}

struct TriviaView_Previews: PreviewProvider {
    static var previews: some View {
        TriviaView()
            .environmentObject(TriviaManager())
    }
}
