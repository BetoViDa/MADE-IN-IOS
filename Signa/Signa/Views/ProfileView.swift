//
//  ProfileView.swift
//  ToCombine
//
//  Created by Victoria Lucero on 12/11/22.
//

import SwiftUI

struct ProfileView: View {

    let signaColor = Color(red: 48/256, green: 212/256, blue: 200/256)

    @State var currentProgress: CGFloat = 0.0
    @State var calis : Calificaciones?
    @State var groupCode : String = ""

    @State private var presentPopup = false

    struct Respuesta : Codable {
        var msj : String
        var group : String
    }

    func unirseGrupo(){
        guard let url = URL(string: APIURL + "/user/joinGroup") else{
            return
        }//ponemos el url de la api en una variable string
        let body: [String:AnyHashable] = [
            "_id" : logedUser._id,
            "groupCode": self.groupCode
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
                let response = try JSONDecoder().decode(Respuesta.self, from: data)
                if(response.group != "None"){
                    logedUser.group = response.group
                }
                print(response.msj)
            }
            catch{
                print("Error al unirse al grupo")
            }
        
        }   
        task.resume()
    }

    func sacarCalificaciones(){
        guard let url = URL(string: APIURL + "/user/grades/\(logedUser._id)") else{
            return
        }//ponemos el url de la api en una variable string
        let request = URLRequest(url: url)
        URLSession.shared.dataTask(with: request) { data, response, error in
            if let data = data {
                if let response = try? JSONDecoder().decode(Calificaciones.self, from: data) {
                    DispatchQueue.main.async{
                        self.calis = response
                    }
                    return
                }
            }
        }.resume()
    }
    
    struct Calificaciones : Codable {
        var grades : [Cali]
    }
    struct Cali : Codable {
        var name : String
        var grade : Float
    }
    
    
    
     

    var body: some View {
        ZStack{
            VStack {
                if(logedUser.lvl == 19){
                    Image("goldcup")
                    .scaleEffect(0.2)
                    .frame(width:100, height: 100)
                    .scaledToFit()
                    .clipShape(Circle())
                    .overlay {
                        Circle().stroke(.white, lineWidth: 4)
                    }
                    .shadow(radius: 7)
                } else if (logedUser.lvl >= 9) {
                    Image("silvcup")
                    .scaleEffect(0.2)
                    .frame(width:100, height: 100)
                    .scaledToFit()
                    .clipShape(Circle())
                    .overlay {
                        Circle().stroke(.white, lineWidth: 4)
                    }
                    .shadow(radius: 7)
                }else if (logedUser.lvl >= 4){
                    Image("broncup")
                    .scaleEffect(0.2)
                    .frame(width:100, height: 100)
                    .scaledToFit()
                    .clipShape(Circle())
                    .overlay {
                        Circle().stroke(.white, lineWidth: 4)
                    }
                    .shadow(radius: 7)
                }else{
                    Image("earth3")
                    .scaleEffect(0.5)
                    .frame(width:100, height: 100)
                    .scaledToFit()
                    .clipShape(Circle())
                    .overlay {
                        Circle().stroke(.white, lineWidth: 4)
                    }
                    .shadow(radius: 7)
                }


                VStack{
                Text("\(logedUser.username)")
                    .font(.title)
                    .fontWeight(.bold)
                    .padding()
                
                HStack {
                    if(logedUser.group != ""){
                        Text("Grupo: \(logedUser.group)")
                            .font(.title2)
                    }else { 
                        Button ( action:{
                                self.presentPopup = true
                        }){
                            Text("No te encuentras en un grupo 😔")
                            .font(.subheadline)
                                .foregroundColor(.white)
                                .frame(alignment: .center)
                                .padding()
                                
                        }
                        .background(signaColor)
                        .padding(5)
                        .containerShape(Capsule())
                        
                    }

                    Spacer()
                    Text("Nivel: \(logedUser.lvl)")
                        .font(.subheadline)
                }
                    .font(.subheadline)
                    .foregroundColor(.secondary)
                
                
                Divider()
    
            }
            .onAppear(){
                sacarCalificaciones()
            }
            .padding()
                
                //Esto es prueba
                ScrollView(){
                    if calis != nil{
                        ForEach((0...(calis!.grades.count - 1)), id: \.self){ grade in
                            VStack(alignment: .center){
                                Spacer()
                                Spacer()
                                HStack {
                                    Text(calis!.grades[grade].name)
                                        .padding(.horizontal)
                                    Text(String(format: "%.2f",calis!.grades[grade].grade) + " %")
                                }
                                ZStack(alignment: .leading) {
                                    RoundedRectangle(cornerRadius: 20)
                                        .foregroundColor(.gray)
                                        .frame(width: 300, height: 20)
                                    RoundedRectangle(cornerRadius: 20)
                                                    .foregroundColor(signaColor)
                                                    .frame(width: CGFloat((300*(calis!.grades[grade].grade)))/100, height: 20)
                                    
                                }
                            }
                        }
                    }
                }
                Spacer()
            }
        }
        if presentPopup{
            VStack(spacing: 50){
                Text("Unirse a un grupo")
                TextField("Codigo", text:
                                $groupCode).padding().background(Capsule()
                                    .strokeBorder(Color.gray,lineWidth: 0.8)
                                    .background(Color.white)
                                    .clipped()).cornerRadius(5.0).padding(.horizontal,30.0)
                HStack{
                    Button(action : {
                        withAnimation {
                            unirseGrupo()
                            self.presentPopup = false
                        }
                    }, label: {
                        Text("Unirse")
                            .foregroundColor(.white)
                            .frame(alignment: .center)
                            .padding()
                    })
                        .background(signaColor)
                        .padding(5)
                        .containerShape(Capsule())
                    Button(action : {
                        withAnimation {
                            self.presentPopup = false
                        }
                    }, label : {
                        Text("Salir")
                            .foregroundColor(.white)
                            .frame(alignment: .center)
                            .padding()
                    })
                        .background(signaColor)
                        .padding(5)
                        .containerShape(Capsule())
                    
                }
            }
        }
        
    }
}
    
struct ProfileView_Previews: PreviewProvider {
    static var previews: some View {
        ProfileView()
    }
}
