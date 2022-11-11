import SwiftUI

struct ContentView : View {
    var body: some View {
        NavigationView {
            VStack {
                Image("logo")
                    .resizable()
                    .scaledToFit()
                    .frame(width:350)
                //.imageScale(.small)
                //.foregroundColor(.accentColor)
                Text("Inicia sesión").font(.system(size:30, weight: .bold, design: .rounded))

                NavigationLink(destination: Login()) {
                    Image("user")
                        .resizable()
                        .scaledToFit()
                        .frame(width:50)
                        .padding(.horizontal,10)
                    Text(  "Iniciar sesión     ").padding(.horizontal,10)
                    
                   
                }.fontWeight(.light)
                    .foregroundColor(.gray)
                    .padding(.top,5)
                    .padding(.bottom,5)
                    .padding(.horizontal,1)
                    .overlay(
                        Capsule(style: .continuous)
                            .stroke(Color.gray, style: StrokeStyle(lineWidth: 2))).frame(width:200)
                
                
                 NavigationLink(destination: SignUp()) {
                     Image("user")
                         .resizable()
                         .scaledToFit()
                         .frame(width:50)
                         .padding(.horizontal,15)
                     Text(  "Registro    ").padding(.horizontal,10)
                     
                    
                 }.fontWeight(.light)
                     .foregroundColor(.gray)
                     .padding(.top,5)
                     .padding(.bottom,5)
                     .padding(.horizontal,1)
                     .overlay(
                         Capsule(style: .continuous)
                             .stroke(Color.gray, style: StrokeStyle(lineWidth: 2))).frame(width:200)
                   
          }
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}

