//
//  DiccionarioView.swift
//  Signa
//
//  Created by Victoria Lucero on 13/11/22.
//

import SwiftUI

struct DiccionarioView: View {
    
    struct Palabras : Codable {
        var palabra : String
    }
    
    @State var topicword : String = ""
    @State var results = [Palabras]()
    
    func loadWord(){
        guard let url = URL(string: "http://127.0.0.1:5000/categories/all/\(topicword)") else {
                    print("Invalid URL")
                    return
                }
        print(url)
                let request = URLRequest(url: url)

                URLSession.shared.dataTask(with: request) { data, response, error in
                    if let data = data {
                        if let response = try? JSONDecoder().decode([Palabras].self, from: data) {
                            DispatchQueue.main.async {
                                self.results = response
                            }
                            return
                        }
                    }
                }.resume()
    }
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(alignment: .center) {
                
                    
                    ScrollView(.horizontal){
                        Group {
                            
                            HStack{
                                Text("Tópicos")
                                    .font(.title)
                                    .fontWeight(.bold)
                                    .multilineTextAlignment(.center).padding()
                                Spacer()
                            }
                            
                            
                            HStack(alignment: .center){
                                Spacer()
                                Button(action: {
                                    print("Boton ABC precionado")
                                    topicword = "letras"
                                }){
                                    Image("abc")
                                        .scaleEffect(0.18)
                                        .frame(width:100, height: 100)
                                        .scaledToFit()
                                        .clipShape(Circle())
                                        .overlay {
                                            Circle().stroke(.white, lineWidth: 4)
                                        }
                                        .shadow(radius: 7)
                                }
                                Spacer()
                                Button(action: {
                                    print("Boton Preposiciones precionado")
                                }){
                                    Image("5")
                                        .scaleEffect(0.18)
                                        .frame(width:100, height: 100)
                                        .scaledToFit()
                                        .clipShape(Circle())
                                        .overlay {
                                            Circle().stroke(.white, lineWidth: 4)
                                        }
                                        .shadow(radius: 7)
                                }
                                Spacer()
                                Button(action: {
                                    print("Boton VComunes precionado")
                                }){
                                    Image("earth3")
                                        .scaleEffect(0.20)
                                        .frame(width:100, height: 100)
                                        .scaledToFit()
                                        .clipShape(Circle())
                                        .overlay {
                                            Circle().stroke(.white, lineWidth: 4)
                                        }
                                        .shadow(radius: 7)
                                }
                                Spacer()
                                Button(action: {
                                    print("Boton VNarrativos precionado")
                                }){
                                    Image("earth2")
                                        .scaleEffect(0.25)
                                        .frame(width:100, height: 100)
                                        .scaledToFit()
                                        .clipShape(Circle())
                                        .overlay {
                                            Circle().stroke(.white, lineWidth: 4)
                                        }
                                        .shadow(radius: 7)
                                }
                                Spacer()
                                
                                
                            }
                            HStack(alignment: .center){
                                Spacer()
                                Text("ABC")
                                    .font(.title2)
                                    .fontWeight(.semibold).padding()
                                Spacer()
                                Text("Preposiciones")
                                    .font(.title2)
                                    .fontWeight(.semibold)
                                    .padding()
                                Spacer()
                                Text("Verbos Comunes")
                                    .font(.title2)
                                    .fontWeight(.semibold).padding()
                                Spacer()
                                Text("Verbos Narrativos")
                                    .font(.title2)
                                    .fontWeight(.semibold).padding()
                                Spacer()
                            }
                        }
                    }
                    Spacer()
                    
                    
                    
                    
                    Group {
                        HStack{
                            Text("Palabras")
                                .font(.title)
                                .fontWeight(.bold)
                                .multilineTextAlignment(.center).padding()
                            Spacer()
                        }
                    
                        HStack(alignment: .center){
                            Spacer()
                            Text("Palabra1")
                                .font(.title2)
                                .fontWeight(.semibold).padding()
                            Spacer()
                            Text("Palabra2")
                                .font(.title2)
                                .fontWeight(.semibold)
                                .padding()
                            Spacer()
                            Text("Palabra3")
                                .font(.title2)
                                .fontWeight(.semibold).padding()
                            Spacer()
                        }
                        
                        HStack(alignment: .center){
                            Spacer()
                            Text("Palabra4")
                                .font(.title2)
                                .fontWeight(.semibold).padding()
                            Spacer()
                            Text("Palabra5")
                                .font(.title2)
                                .fontWeight(.semibold)
                                .padding()
                            Spacer()
                            Text("Palabra6")
                                .font(.title2)
                                .fontWeight(.semibold).padding()
                            Spacer()
                        }
                        
                        
                        
                        
                    }
                }
            }.navigationTitle("Diccionario").navigationBarTitleDisplayMode(.automatic)
        }
    }
}

struct DiccionarioView_Previews: PreviewProvider {
    static var previews: some View {
        DiccionarioView()
    }
}
