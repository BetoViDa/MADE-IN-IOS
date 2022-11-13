//
//  Login.swift
//  loginswift
//
//  Created by Victoria Lucero on 09/11/22.
//

import SwiftUI

struct Login: View {
    struct Error: Codable{
        var ERROR : String
    }
    
    @State var errorMsj: String = ""
    @State var username: String = ""
    @State var password: String = "";
    
    func APILogIn(){
        
        guard let url = URL(string: APIURL + "/user/login") else{
            return
        }//ponemos el url de la api en una variable string
        let body: [String:AnyHashable] = [
            "username" : username,
            "password": password
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
                // en este do intentaremos crear el usuario
                let response = try JSONDecoder().decode(User.self, from: data)// tratamos de decodearlo en una estructura de tipo User
                logedUser = response
                errorMsj = ""
            }
            catch{
                // si no se pudo crear el usuario
                // recibimos un error
                let response = try? JSONDecoder().decode(Error.self, from: data)
                errorMsj = response!.ERROR
            }
            
        }
        task.resume()
        
    }
    
    var body: some View {
        
        VStack{
            Image("logoSigna").resizable().frame(width: 400, height:400)
            Text("\(errorMsj)")
            TextField("Username", text:
                        $username).padding().background(.cyan).cornerRadius(10.0).padding(.bottom,20)
            SecureField("Password", text: $password).padding().background(.cyan).cornerRadius(5.0).padding(.bottom, 20)
            
            Button("Entrar", action: APILogIn)
            Spacer()
        }
        
    }
}

struct Login_Previews: PreviewProvider {
    static var previews: some View {
        Login()
    }
}
