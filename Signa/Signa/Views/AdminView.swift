//
//  ProfileView.swift
//  ToCombine
//
//  Created by Victoria Lucero on 12/11/22.
//

import SwiftUI

struct AdminView: View {

    let signaColor = Color(red: 48/256, green: 212/256, blue: 200/256)

    @State var currentProgress: CGFloat = 0.0
    @State var calis : Calificaciones?
    @State var groupCode : String = ""
    @State var promedio : Float = 0

    @State private var presentPopup = false

    struct Respuesta : Codable {
        var msj : String
        var group : String
    }
    struct Calificaciones : Codable {
        var grades : [Cali]
    }
    struct Cali : Codable {
        var name : String
        var grade : Float
    }
    

    func sacarCalificaciones(){
        let str = logedUser.group.replacingOccurrences(of: " ", with: "%20")
        print(str)
        guard let url = URL(string: APIURL + "/group/\(str)") else{
            return
        }//ponemos el url de la api en una variable string
        let request = URLRequest(url: url)
        URLSession.shared.dataTask(with: request) { data, response, error in
            if let data = data {
                if let response = try? JSONDecoder().decode(Calificaciones.self, from: data) {
                    DispatchQueue.main.async{
                        self.calis = response
                        // sacar promedio
                        promedio = 0
                        for i in 0...response.grades.count - 1{
                            promedio = promedio + response.grades[i].grade
                        }
                        promedio = promedio / Float(response.grades.count)
                    }
                    return
                }
            }
        }.resume()
    }
    
    @State var showview: Bool = false
    
    func sacofunction(){
        showview = true
    }
     

    var body: some View {
        NavigationView{
            ZStack{
                VStack {
                    HStack{
                        NavigationLink(destination: usersList(), isActive: $showview){
                                Text("")
                        }
                        Spacer()
                        Button(action:{
                            sacofunction()
                        }, label: {
                            Text("Mis alumnos")
                                .padding(.horizontal)
                        })
                    }
                    if(promedio >= 90){
                        Image("goldcup")
                            .scaleEffect(0.2)
                            .frame(width:100, height: 100)
                            .scaledToFit()
                            .clipShape(Circle())
                            .overlay {
                                Circle().stroke(.white, lineWidth: 4)
                            }
                            .shadow(radius: 7)
                    } else if (promedio >= 50) {
                        Image("silvcup")
                            .scaleEffect(0.2)
                            .frame(width:100, height: 100)
                            .scaledToFit()
                            .clipShape(Circle())
                            .overlay {
                                Circle().stroke(.white, lineWidth: 4)
                            }
                            .shadow(radius: 7)
                    }else if (promedio >= 20){
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
                        Image("earth")
                            .scaleEffect(0.2)
                            .frame(width:100, height: 100)
                            .scaledToFit()
                            .clipShape(Circle())
                            .overlay {
                                Circle().stroke(.white, lineWidth: 4)
                            }
                            .shadow(radius: 7)
                    }
                    
                    
                    VStack(alignment: .center, spacing: 20){
                        Text("\(logedUser.username)")
                            .font(.system(size:15, weight: .semibold, design: .rounded)).foregroundColor(.gray)
                        HStack {
                            Text("Grupo: ")
                                .font(.title)
                                .fontWeight(.bold).foregroundColor(.gray)
                            Text("\(logedUser.group)")
                                .font(.title)
                                .fontWeight(.bold).foregroundColor(Color("AccentColor"))
                        }
                        .font(.system(size:20, weight: .semibold, design: .rounded))
                        
                       
                        
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
        }.navigationBarBackButtonHidden(true)
    }
}
    
struct AdminView_Previews: PreviewProvider {
    static var previews: some View {
        AdminView()
    }
}

