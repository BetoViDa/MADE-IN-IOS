//
//  usersList.swift
//  Signa
//
//  Created by Macías Romero on 28/11/22.
//

import SwiftUI



struct usersList: View {
    
    let signaColor = Color(red: 48/256, green: 212/256, blue: 200/256)
    
    @State var lu : Userslist?
    @State var showUserInfo : Bool = false
    @State var analGrades : Grades?
    @State var lvlUser : Int = 0
    @State var userA : String = ""
    
    struct Grade: Codable {
        var grade : Float
        var name : String
    }
    struct Grades: Codable {
        var grades : [Grade]
    }
    
    struct User: Codable {
        var _id : String
        var lvl : Int
        var username : String
    }
    
    struct Userslist: Codable {
        var usersL : [User]
    }
    
    
    func infoUser(idUser : String){
        guard  let url = URL(string: APIURL + "/user/grades/\(idUser)") else{
            return
        }
        let request = URLRequest(url: url)
        URLSession.shared.dataTask(with: request) { data, response, error in
            if let data = data {
                if let response = try? JSONDecoder().decode(Grades.self, from: data) {
                    DispatchQueue.main.async{
                        self.analGrades = response
                    }
                    return
                }
            }
        }.resume()
    }
    
    func sacarLista(){
        let str = logedUser.group.replacingOccurrences(of: " ", with: "%20")
        guard let url = URL(string: APIURL + "/user/users/\(str)") else{
            return
        }
        let request = URLRequest(url: url)
        URLSession.shared.dataTask(with: request) { data, response, error in
            if let data = data {
                if let response = try? JSONDecoder().decode(Userslist.self, from: data) {
                    DispatchQueue.main.async{
                        self.lu = response
                        print(response)
                    }
                    return
                }
            }
        }.resume()
    }
    
    var body: some View {
        Spacer()
        Text("Usuarios de \(logedUser.group)")
            .font(.title)
            .fontWeight(.bold)
        ScrollView{
            VStack{
                Spacer(minLength: 6.0)
                if lu != nil{
                        ForEach((0...((lu?.usersL.count)!-1)), id: \.self){index in
                            Group{
                              
                                    HStack(alignment: .center, spacing: 4){
                                        
                                        
                                        Button("\(lu!.usersL[index].username)"){
                                            infoUser(idUser: (lu?.usersL[index]._id)!)
                                            self.userA = lu!.usersL[index].username
                                            self.lvlUser = lu!.usersL[index].lvl
                                            showUserInfo = true
                                        }.font(.system(size:22, weight: .bold, design: .rounded)).foregroundColor(.white).padding(.horizontal,10)
                                        Spacer()
                                        Text("Nivel: \(lu!.usersL[index].lvl)").padding(.horizontal).font(.system(size:22, weight: .bold, design: .rounded)).foregroundColor(.white).padding(.horizontal,5)
                                        
                                       
                                    }.font(.title3)
                                        .overlay(
                                            Capsule(style: .continuous)
                                                .stroke(Color("AccentColor"), style: StrokeStyle(lineWidth: 2))).padding(.top,4).padding(.bottom,5)
                                        .background(Capsule().fill(Color("AccentColor")))
                                        .frame(width:300).padding(.horizontal)
                                
                                
                            }.padding(.top, 10)
                        }
                        Spacer()
                }
            }.onAppear(){
                sacarLista()
            }
            .popover(isPresented: $showUserInfo){
                ZStack{
                                VStack {
                                    if(lvlUser == 19){
                                        Image("goldcup")
                                            .scaleEffect(0.2)
                                            .frame(width:100, height: 100)
                                            .scaledToFit()
                                            .clipShape(Circle())
                                            .overlay {
                                                Circle().stroke(.white, lineWidth: 4)
                                            }
                                            .shadow(radius: 7)
                                            .padding(.top)
                                    } else if (lvlUser >= 9) {
                                        Image("silvcup")
                                            .scaleEffect(0.2)
                                            .frame(width:100, height: 100)
                                            .scaledToFit()
                                            .clipShape(Circle())
                                            .overlay {
                                                Circle().stroke(.white, lineWidth: 4)
                                            }
                                            .shadow(radius: 7)
                                            .padding(.top)
                                    }else if (lvlUser >= 4){
                                        Image("broncup")
                                            .scaleEffect(0.2)
                                            .frame(width:100, height: 100)
                                            .scaledToFit()
                                            .clipShape(Circle())
                                            .overlay {
                                                Circle().stroke(.white, lineWidth: 4)
                                            }
                                            .shadow(radius: 7)
                                            .padding(.top)
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
                                            .padding(.top)
                                    }
                                    
                                    
                                    VStack{
                                        Text("\(userA)")
                                            .font(.system(size:20, weight: .bold, design: .rounded))
                                            .padding()
                                        
                                        Divider()
                                        
                                    }
                                    .padding()
                                    
                                    //Esto es prueba
                                    ScrollView(){
                                        if analGrades != nil{
                                            ForEach((0...(analGrades!.grades.count - 1)), id: \.self){ grade in
                                                VStack(alignment: .center){
                                                    Spacer()
                                                    Spacer()
                                                    HStack {
                                                        Text(analGrades!.grades[grade].name)
                                                            .padding(.horizontal)
                                                        Text(String(format: "%.2f",analGrades!.grades[grade].grade) + " %")
                                                    }
                                                    ZStack(alignment: .leading) {
                                                        RoundedRectangle(cornerRadius: 20)
                                                            .foregroundColor(.gray)
                                                            .frame(width: 300, height: 20)
                                                        RoundedRectangle(cornerRadius: 20)
                                                            .foregroundColor(signaColor)
                                                            .frame(width: CGFloat((300*(analGrades!.grades[grade].grade)))/100, height: 20)
                                                        
                                                    }
                                                }
                                            }
                                        }
                                    }
                                    Spacer()
                                }
                            }
            }
        }
    }
    
    
    
}

struct usersList_Previews: PreviewProvider {
    static var previews: some View {
        usersList()
    }
}
