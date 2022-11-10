//
//  Login.swift
//  loginswift
//
//  Created by Victoria Lucero on 09/11/22.
//

import SwiftUI


struct Login: View {
    @State var username: String = "vic"
    @State var password: String = "123";
      

      
    var body: some View {
        
        VStack{
            Image("logoSigna").resizable().frame(width: 400, height:400)
            Spacer()
            TextField("Username", text:
                        $username).padding().background(.cyan).cornerRadius(10.0).padding(.bottom,20)
            SecureField("Password", text: $password).padding().background(.cyan).cornerRadius(5.0).padding(.bottom, 20)
            
            Spacer()
            NavigationLink(destination: Main()) {
                Text("Login")
                    .frame(minWidth: 0, maxWidth: 300)
                    .padding()
                    .border(.gray,width:2)
                    .foregroundColor(.gray)
                    .background(.white)
                    .cornerRadius(40)
                    .font(.title)
                
            }
        }
        
    }

      struct SecondView_Previews: PreviewProvider {
          static var previews: some View {
              SecondView()
          }
    }
}

struct Login_Previews: PreviewProvider {
    static var previews: some View {
        Login()
    }
}
