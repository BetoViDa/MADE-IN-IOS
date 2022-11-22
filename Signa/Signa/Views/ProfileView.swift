//
//  ProfileView.swift
//  ToCombine
//
//  Created by Victoria Lucero on 12/11/22.
//

import SwiftUI

struct ProfileView: View {
    @State var currentProgress: CGFloat = 0.0

    @State var calis : Calificaciones?

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
        
        VStack {
            Image("earth3")
                .scaleEffect(0.5)
                .frame(width:100, height: 100)
                .scaledToFit()
                .clipShape(Circle())
                .overlay {
                    Circle().stroke(.white, lineWidth: 4)
                }
                .shadow(radius: 7)
            VStack{
            Text("\(logedUser.username)")
                .font(.title)
                .fontWeight(.bold)
                .padding()
            
               HStack {
                   if(logedUser.group != ""){
                       Text("Grupo: \(logedUser.group)")
                           .font(.title2)
                   } else {
                       Text("No te encuentras en un grupo 😔")
                           .font(.subheadline)
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
                                                .foregroundColor(.blue)
                                                .frame(width: CGFloat((300*(calis!.grades[grade].grade)))/100, height: 20)
                                
                            }
                        }
                    }
                }
            }
            Spacer()
        }
    }
}
    
struct ProfileView_Previews: PreviewProvider {
    static var previews: some View {
        ProfileView()
    }
}
