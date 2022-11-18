//
//  PRUEBAIMAGEN.swift
//  Signa
//
//  Created by Macías Romero on 16/11/22.
//

import SwiftUI
import AVKit

struct PRUEBAIMAGEN: View {
    
    /*
    struct Palabras : Codable {
        var palabra : [String]
    }
    
    @State var topicword : String = ""
    @State var results : Palabras?
    //var resultados : [Palabras]
    
    func loadIMG(){
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
    }  */
    
    var urldrive = "https://drive.google.com/uc?export=view&id="
    var idfile = "1fwjznopswbFUHAnWYzIZXIE1TPIPPWkp"

    var body: some View {
        AsyncImage(url: URL(string:urldrive + idfile)){ phase in
            if let image = phase.image {
                image // Cuando el file es IMAGEN
            } else if phase.error != nil {
                // Cuando el file es VIDEO
                VideoPlayer(player: AVPlayer(url: URL(string: urldrive + idfile)!))
            }
        }
    }
}

struct PRUEBAIMAGEN_Previews: PreviewProvider {
    static var previews: some View {
        PRUEBAIMAGEN()
    }
}
