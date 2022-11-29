
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
                Text("Inicia sesión").font(.system(size:30, weight: .bold, design: .rounded)).foregroundColor(Color("adb5bd"))
                
                NavigationLink(destination: Login()) {
                    
                        Image(systemName: "person.crop.circle.fill")
                            .resizable()
                            .scaledToFit()
                            .frame(width:40)
                            .padding(.horizontal,5)
                            .foregroundColor(.white)
                    Text(  "Iniciar sesión     .").foregroundColor(.white).fontWeight(.semibold)
                    
                   
                    
                   
                }.fontWeight(.light)
                    .foregroundColor(.gray)
                    .padding(.top,5)
                    .padding(.bottom,5)
                    .padding(.horizontal,1)
                    .overlay(
                        Capsule(style: .continuous)
                            .stroke(Color("AccentColor"), style: StrokeStyle(lineWidth: 2)))
                    .background(Capsule().fill(Color("AccentColor")))
                    .frame(width:200)
                
                
                NavigationLink(destination: SignUp()) {
                                     Image(systemName: "plus.circle.fill")
                                         .resizable()
                                         .scaledToFit()
                                         .frame(width:40)
                                         .padding(.horizontal,6)
                                         .foregroundColor(Color("adb5bd"))
                                     Text(  "Registro             .").foregroundColor(Color("adb5bd")).fontWeight(.semibold)
                                     
                                    
                                 }.fontWeight(.light)
                                     .foregroundColor(.gray)
                                     .padding(.top,5)
                                     .padding(.bottom,5)
                                     .padding(.horizontal,1)
                                     .overlay(
                                         Capsule(style: .continuous)
                                             .stroke(Color("adb5bd"), style: StrokeStyle(lineWidth: 2))).frame(width:200)
                   
          }
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
