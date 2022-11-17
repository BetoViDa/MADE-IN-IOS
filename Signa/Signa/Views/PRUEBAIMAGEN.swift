//
//  PRUEBAIMAGEN.swift
//  Signa
//
//  Created by Macías Romero on 16/11/22.
//

import SwiftUI

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
    
    var urldrive = "https://drive.google.com/file/d/"

    var body: some View {
        AsyncImage(url: URL(string: "https://drive.google.com/file/d/1QKqGSkKy5a7CYT0hmX9u-kFHB7wP-5_M")){ phase in
            if let image = phase.image {
                image // Displays the loaded image.
            } else if phase.error != nil {
                Color.red // Indicates an error.
            } else {
                Color.blue // Acts as a placeholder.
            }
        }
    }
}

struct PRUEBAIMAGEN_Previews: PreviewProvider {
    static var previews: some View {
        PRUEBAIMAGEN()
    }
}
