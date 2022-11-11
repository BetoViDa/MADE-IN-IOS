//
//  SignUp.swift
//  loginswift
//
//  Created by Victoria Lucero on 09/11/22.
//

import SwiftUI
import UIKit


struct SignUp: View {
    
    struct Mensajes : Codable {
        var msj : String
        var ERROR : String
    }
    
    @State var username: String = ""
    @State var password: String = ""
    @State var email: String = ""
  
    func makePostRequest(){
        guard let url = URL(string: APIURL + "/user/signup") else{
            return
        }
        var request = URLRequest(url:url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        let body: [String:AnyHashable] = [
            "username" : username,
            "email": email,
            "password": password
        ]
        request.httpBody = try? JSONSerialization.data(withJSONObject: body, options: .fragmentsAllowed)
        //Make the request
        let task = URLSession.shared.dataTask(with: request) {data, _, error in
            guard let data = data, error == nil else{
                return
            }
            do {
                let response = try JSONDecoder().decode(Mensajes.self, from:    data)
                
                if (response.ERROR != "no"){
                    //MOSTRAR MENSAJE DE ERROR EN ROJO
                    print(response.ERROR)
                } else {
                    //ME MANDARA A LOGIN
                    print(response.msj)
                }

                /*
                NavigationLink(destination: Login()) {
                    Text("REGISTRATE")
                    
                    .frame(minWidth: 0, maxWidth: 300)
                    .padding()
                    .border(.gray,width:2)
                    .foregroundColor(.gray)
                    .background(.white)
                    .cornerRadius(0)
                    .font(.title)
                }
                 */
                
            } catch {
                print(error)
            }
        }
        task.resume()
    }
    
    
    var body: some View {
        VStack{
            Image("logoSigna").resizable().frame(width: 400, height:400)
            Spacer()
            TextField("Username", text: $username).padding().background(.cyan).cornerRadius(10.0).padding(.bottom,20)
            TextField("Email", text: $email).padding().background(.cyan).cornerRadius(10.0).padding(.bottom,20)
            SecureField("Password", text: $password).padding().background(.cyan).cornerRadius(5.0).padding(.bottom, 20)
            Spacer()
            Button("Registrateeeeee", action: makePostRequest)
        }
    }
}

struct SignUp_Previews: PreviewProvider {
    static var previews: some View {
        SignUp()
    }
}
