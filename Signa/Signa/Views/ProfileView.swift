//
//  ProfileView.swift
//  ToCombine
//
//  Created by Victoria Lucero on 12/11/22.
//

import SwiftUI

struct ProfileView: View {
    @State var currentProgress: CGFloat = 0.0
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
            Text("Turtle Rock")
                .font(.title)
                .fontWeight(.bold)

                       HStack {
                           Spacer()
                           Text("Nivel 1")
                               .font(.subheadline)
            }
               .font(.subheadline)
               .foregroundColor(.secondary)

            Divider()
            VStack(alignment: .leading){
                
                HStack(alignment: .top) {
                    Text("Description")
                        .font(.title2)
                    .fontWeight(.semibold)
                    Spacer()
                }
                Text("Descriptive text goes here.")
                    .foregroundColor(.secondary)
          
            }
                   }
                   .padding()
            
            //Esto es prueba
            VStack{
                Text("ABC1")
                ZStack(alignment: .leading) {
                    RoundedRectangle(cornerRadius: 20)
                        .foregroundColor(.gray)
                        .frame(width: 300, height: 20)
                    RoundedRectangle(cornerRadius: 20)
                                    .foregroundColor(.blue)
                                    .frame(width: 300*0.50, height: 20)
                    
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
