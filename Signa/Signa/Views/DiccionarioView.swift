//
//  DiccionarioView.swift
//  Signa
//
//  Created by Victoria Lucero on 13/11/22.
//

import SwiftUI
import WrappingHStack

struct DiccionarioView: View {
    
    var imagenes = ["abc","5","earth3","earth2"]
    let signa = Color(red: 48/256, green: 212/256, blue: 200/256)

    //PUEDE CAMBIARSE POR UN JSON...
    var namestopics = ["ABC", "Preposiciones", "Verbos Comunes", "Verbos Narrativos"]
    var topicos = ["letras", "preposiciones", "verboscomunes", "verbosnarrativos"]
    
    
    //PARA EL TAMANIO DE LOS TEXTOS
    var topicsSize : [Font] = [.title2,.title2,.title3,.system(size: 19)]
    
    struct Palabras : Codable {
        var palabra : [String]
    }
    
    @State var topicword : String = ""
    @State var results : Palabras?
    //var resultados : [Palabras]
    
    func loadWord(){
        guard let url = URL(string: "http://127.0.0.1:5000/categories/all/\(topicword)") else {
                    print("Invalid URL")
                    return
                }
                let request = URLRequest(url: url)

                URLSession.shared.dataTask(with: request) { data, response, error in
                    if let data = data {
                        if let response = try? JSONDecoder().decode(Palabras.self, from: data) {
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
                            /*
                            HStack{
                                Text("Tópicos")
                                    .font(.title)
                                    .fontWeight(.bold)
                                    .multilineTextAlignment(.center).padding()
                                Spacer()
                            }
                            */
                            
                            HStack(alignment: .center){
                                ForEach((0...3), id: \.self){index in
                                    VStack(alignment: .center){
                                        Button(action: {
                                            topicword = topicos[index]
                                            loadWord()
                                            
                                        }){
                                            Image(imagenes[index])
                                                .scaleEffect(0.18)
                                                .frame(width:100, height: 100)
                                                .scaledToFit()
                                                .clipShape(Circle())
                                                .overlay {
                                                    Circle().stroke(.white, lineWidth: 4)
                                                }
                                                .shadow(radius: 7)
                                        }
                                        Text(namestopics[index])
                                            .font(topicsSize[index])
                                            .fontWeight(.semibold).padding()
                                    }.frame(minWidth: 195, maxWidth: 200, minHeight: 195, maxHeight: 200, alignment: .center)
                                        
                                }
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
                        
                        if results != nil {
                            WrappingHStack(results!.palabra, id:\.self, alignment: .center) { resultados in
                                Button( action: {
                                    //ESTO SE CAMBIARA V
                                    print("SE MUESTRA IMAGEN/VIDEO. Fue presionado la palabra: " + resultados)
                                }){
                                    Text(resultados)
                                        .font(.title2)
                                        .fontWeight(.bold)
                                        .foregroundColor(Color.white)
                                            .frame(width: 130, height: 50, alignment: .center)
                                            .background(signa)
                                            .containerShape(Capsule())
                                            .padding()
                                }
                            }.frame(minWidth: 250)
                        }
                    }
                }
            }.navigationTitle("Tópicos").navigationBarTitleDisplayMode(.automatic)
        }
    }
}

struct DiccionarioView_Previews: PreviewProvider {
    static var previews: some View {
        DiccionarioView()
    }
}
