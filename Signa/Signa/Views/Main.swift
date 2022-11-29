//
//  ContentView.swift
//  ToCombine
//
//  Created by Victoria Lucero on 12/11/22.
//

import SwiftUI


struct Main: View {
    @State var selectedIndex = 0
    
    let icons = ["graduationcap", "book", "person"]
    let vartitles = ["Aprende", "Diccionario", "Perfil"]
    
    
    var body: some View {
        NavigationView{
            VStack {
                //Content
                ZStack{
                    switch selectedIndex{
                    case 0:
                        NavigationView {
                            VStack{
                                AprenderView()
                            }
                        }
                    case 1:
                        NavigationView {
                            VStack{
                                DiccionarioView()
                            }
                        }
                        
                    default:
                        NavigationView {
                            VStack{
                                ProfileView()
                            }
                        }
                    }
                    
                }
                
                
                Divider()
                //Navbar()
                HStack {
                    ForEach(0..<3, id:  \.self) { number in
                        
                        Button(action: {
                            self.selectedIndex = number
                        }, label: {
                            Spacer()
                            
                            Image(systemName: icons[number])
                                .font(.system(size: 25,weight: .regular, design: .default) )
                                .foregroundColor( selectedIndex == number ? Color("AccentColor") : Color(UIColor.lightGray))
                            
                            Spacer()
                        }
                               
                               
                        ).padding(.horizontal, 1).padding(.top, 10)
                        
                    }
                    
                }.background(.white)
                
                HStack{
                    ForEach(0...2, id: \.self){index in
                        Spacer()
                        Text("\(vartitles[index])")
                            .font(.system(size: 15))
                            .foregroundColor(selectedIndex == index ? Color("AccentColor") : Color(UIColor.lightGray))
                        Spacer()
                        Spacer()
                    }
                }
                
            }
        }.navigationBarBackButtonHidden(true)
    }
}


struct Main_Previews: PreviewProvider {
    static var previews: some View {
        Main()
    }
}
