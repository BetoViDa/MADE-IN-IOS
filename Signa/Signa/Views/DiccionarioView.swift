//
//  DiccionarioView.swift
//  Signa
//
//  Created by Victoria Lucero on 13/11/22.
//

import SwiftUI
import AVKit
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
    struct Archivo : Codable {
        var file : String
        var fileType : Bool 
    }
    @State var topicword : String = "letras1"
    @State var results : Palabras?
    @State var archivoID : Archivo?

    @State private var presentPopup = false
    @State private var palabraSelec = ""
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

    //=======================================================================

    func loadArchivo(palabra: String){
        //
        self.palabraSelec = palabra
        guard let url = URL(string: "http://127.0.0.1:5000/categories/file/\(topicword)/\(palabra)") else {
                    print("Invalid URL")
                    return
                }
                let request = URLRequest(url: url)

                URLSession.shared.dataTask(with: request) { data, response, error in
                    if let data = data {
                        if let response = try? JSONDecoder().decode(Archivo.self, from: data) {
                            self.archivoID = response
                            return
                        }
                    }
                }.resume()
        
    }
    
    var body: some View {
        ZStack{

            NavigationView {
                ScrollView {
                    VStack(alignment: .center) {
                    

                        ScrollView(.horizontal){
                            Group {
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
                        .onAppear(){
                            loadWord()
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
                                        loadArchivo(palabra: resultados)
                                        self.presentPopup = true
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
        if presentPopup {
            //popup view
            VStack(spacing : 10){
                Text("Palabra: " + self.palabraSelec)
                
                if((archivoID?.fileType) != nil){ // true = image
                    
                    if (((archivoID?.file) != nil) && archivoID?.fileType == true) {
                        // mostramos una imagen
                        AsyncImage(url: URL(string: UrlDriveFiles + archivoID!.file)){ image in
                            image.resizable().frame(width: 200, height: 100)
                        } placeholder: {
                            ProgressView()
                        }
                    } else if (((archivoID?.file) != nil) && archivoID?.fileType == false) {
                        VideoPlayer(player: AVPlayer(url: URL(string: UrlDriveFiles + archivoID!.file)!))
                            .frame(width: 300, height: 120)
                    }
                    
                }
                Button(action : {
                    withAnimation {
                        self.presentPopup = false
                    }
                }, label: {
                    Text("Cerrar")
                })
            }
        }
    }
}

struct DiccionarioView_Previews: PreviewProvider {
    static var previews: some View {
        DiccionarioView()
    }
}
