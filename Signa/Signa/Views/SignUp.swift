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
    @State var msjError: String = ""
    @State var msjErrorMail: String = ""
    @State var msjErrorNombre: String = ""
    @State var msjErrorContra: String = ""
    @State var msjErrorSignUp: String = ""
    @State var showView: Bool = false
    
    
    func makePostRequest(){
        // si falta aglun campo mostramos un error
        if(username == "" || email == "" || password == ""){
            msjError = ("Faltan campos de llenar")
        }
        else{ // no hay error
            msjError = "" // si se mostraba un error, y ya no se cumple volvemos a ocultarlo
        }
        // checar si se cumple con un buen correo, username y constrasenia
        
        //-----checar que el email sea valido-----
        let emailRegEx = "[A-Z0-9a-z._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,64}" // expresion regular
        let emailPred = NSPredicate(format:"SELF MATCHES %@", emailRegEx)
        if(!emailPred.evaluate(with: email)){ // mail invalido
            msjErrorMail = "Email no valido"
        }
        else{// no hay error
            msjErrorMail = ""
        }
        //=======================================
        
        //---checamos que user este correcto------
        let userRegEx = "[A-Z0-9a-z_/]{3,16}"
        let userPred = NSPredicate(format:"SELF MATCHES %@", userRegEx)
        if(!userPred.evaluate(with: username)){ // username invalido
            msjErrorNombre = "Tu nombre debe contener entre 3 y 16 caracteres y solo usar letras, numeros, _, /"
        }
        else{
            msjErrorNombre = ""
        }
        //========================================
        //--------Error con password--------------
        let passwordRegEx = "(?=.*[A-Za-z])(?=.*\\d)(?=.*[@$!%*#?&])[A-Za-z\\d@$!%*#?&]{8,}"
        //Minimum eight characters, at least one letter, one number and one special character:
        let passwordPred = NSPredicate(format:"SELF MATCHES %@", passwordRegEx)
        if(!passwordPred.evaluate(with: password)){
            msjErrorContra = "Minimo 8 caracteres, una letra, un numero, y un caracter especail Solo se aceptan (@$!%*#?&)"
        }
        else{
            msjErrorContra = ""
        }
        //========================================
        
        //--------si hay error no continuamos----------
        if(msjError != "" || msjErrorMail != "" || msjErrorContra != "" || msjErrorNombre != ""){ // si se encontro un error
            print("error por credenciales invalidas") // mostramos un error en consola
            return // no continuamos
        }
        //===============================================
        
        
        //===============================================
        //--------------API--------------------------------
        guard let url = URL(string: APIURL + "/user/signup") else{
            return
        }//ponemos el url de la api en una variable string
        let body: [String:AnyHashable] = [
            "username" : username,
            "email": email,
            "password": password
        ]
        var request = URLRequest(url:url)//lo convertimos en una request para poder poner que es post y un body
        
        request.httpMethod = "POST"//ponemos su metodo como post
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = try? JSONSerialization.data(withJSONObject: body, options: .fragmentsAllowed)//ponemos el body con los datos en el request
        
        //creeamos la task pasandole el request
        let task = URLSession.shared.dataTask(with: request) {data, _, error in
            guard let data = data, error == nil else{
                return
            }
            do {
                
                let response = try JSONDecoder().decode(Mensajes.self, from: data)
                
                if (response.ERROR == "si"){
                    //MOSTRAR MENSAJE DE ERROR EN ROJO
                    msjErrorSignUp = response.msj
                    print(response.msj)
                } else {
                    //ME MANDARA A LOGIN
                    print(response.msj)
                    showView = true

                }

                
            } catch {
                print(error)
            }
        }
        task.resume()
    }
    
    
    var body: some View {

        NavigationView{
            VStack{
                Image("logoSigna").resizable().frame(width: 300, height:200)
                /*
                NavigationLink(destination: Text("Prueba"), tag: "Login", selection: $showView){
                    Login()
                }
                 */
                
                NavigationLink(destination: ContentView().navigationBarBackButtonHidden(false), isActive: $showView){
                    Text("")
                }
                
                ZStack{
                    Text("\(msjErrorSignUp)")
                                Text("\(msjError)").font(.system(size: 9))
                }
                TextField("Username", text: $username).padding().background(Capsule()
                    .strokeBorder(Color.gray,lineWidth: 0.8)
                    .background(Color.white)
                    .clipped()).cornerRadius(10.0).padding(.horizontal,30.0)
                Text("\(msjErrorNombre)").font(.system(size: 9))
                TextField("Email", text: $email).padding().background(Capsule()
                    .strokeBorder(Color.gray,lineWidth: 0.8)
                    .background(Color.white)
                    .clipped()).cornerRadius(5.0).padding(.horizontal,30.0)
                Text("\(msjErrorMail)").font(.system(size: 9))
                SecureField("Password", text: $password).padding().background(Capsule()
                    .strokeBorder(Color.gray,lineWidth: 0.8)
                    .background(Color.white)
                    .clipped()).cornerRadius(5.0).padding(.horizontal,30.0)
                Text("\(msjErrorContra)")
                    .font(.system(size: 9))
                //Spacer()
                Button("Registrate"){
                    makePostRequest()
                }.buttonStyle(.borderedProminent).buttonBorderShape(.capsule).tint(Color.accentColor).foregroundColor(.white).controlSize(.large).fontWeight(.bold)
            }

        }
    }}

struct SignUp_Previews: PreviewProvider {
    static var previews: some View {
        SignUp()
    }
}
