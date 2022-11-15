import SwiftUI


struct AprenderView: View {
    var body: some View {
        
        NavigationView {
            ScrollView {
                VStack(alignment: .center) {


                    Group {
                        HStack{
                            Text("ABC")
                                .font(.title)
                                .fontWeight(.bold)
                                .multilineTextAlignment(.center).padding()
                            Spacer()
                        }
                        
                            
                        HStack(alignment: .center){
                            Spacer()
                            Image("abc")
                                .scaleEffect(0.18)
                                .frame(width:100, height: 100)
                                .scaledToFit()
                                .clipShape(Circle())
                                .overlay {
                                    Circle().stroke(.white, lineWidth: 4)
                                }
                                .shadow(radius: 7)
                            Spacer()
                            
                            Image("panda")
                                .scaleEffect(0.30)
                                .frame(width:100, height: 100)
                                .scaledToFit()
                                .clipShape(Circle())
                                .overlay {
                                    Circle().stroke(.white, lineWidth: 4)
                                }
                                .shadow(radius: 7)
                            Spacer()
                            
                            Image("earth3")
                                .scaleEffect(0.20)
                                .frame(width:100, height: 100)
                                .scaledToFit()
                                .clipShape(Circle())
                                .overlay {
                                    Circle().stroke(.white, lineWidth: 4)
                                }
                                .shadow(radius: 7)
                            Spacer()
                            
                            
                        }
                        HStack(alignment: .center){
                            Spacer()
                            Text("ABC 1")
                                .font(.title2)
                                .fontWeight(.semibold).padding()
                            Spacer()
                            Text("ABC 2")
                                .font(.title2)
                                .fontWeight(.semibold)
                                .padding()
                            Spacer()
                            Text("ABC 3")
                                .font(.title2)
                                .fontWeight(.semibold).padding()
                            Spacer()
                        }
                    }
                    
                    Spacer()
                    


                    
                    Group {
                        HStack{
                            Text("Preposiciones")
                                .font(.title)
                                .fontWeight(.bold)
                                .multilineTextAlignment(.center).padding()
                            Spacer()
                        }
                        
                        HStack(alignment: .center){
                            Spacer()
                            Image("5")
                                .scaleEffect(0.18)
                                .frame(width:100, height: 100)
                                .scaledToFit()
                                .clipShape(Circle())
                                .overlay {
                                    Circle().stroke(.white, lineWidth: 4)
                                }
                                .shadow(radius: 7)
                            Spacer()
                            
                            Image("karate")
                                .scaleEffect(0.20)
                                .frame(width:100, height: 100)
                                .scaledToFit()
                                .clipShape(Circle())
                                .overlay {
                                    Circle().stroke(.white, lineWidth: 4)
                                }
                                .shadow(radius: 7)
                            Spacer()
                            
                            Image("prep")
                                .scaleEffect(0.30)
                                .frame(width:100, height: 100)
                                .scaledToFit()
                                .clipShape(Circle())
                                .overlay {
                                    Circle().stroke(.white, lineWidth: 4)
                                }
                                .shadow(radius: 7)
                            Spacer()
                            
                            
                        }
                        HStack(alignment: .center){
                            Spacer()
                            Text("Prepos 1")
                                .font(.title2)
                                .fontWeight(.semibold).padding()
                            Spacer()
                            Text("Prepos 2")
                                .font(.title2)
                                .fontWeight(.semibold)
                                .padding()
                            Spacer()
                            Text("Prepos 3")
                                .font(.title2)
                                .fontWeight(.semibold).padding()
                            Spacer()
                        }
                        
                        HStack(alignment: .center){
                            Spacer()
                            Image("prep3")
                                .scaleEffect(0.25)
                                .frame(width:100, height: 100)
                                .scaledToFit()
                                .clipShape(Circle())
                                .overlay {
                                    Circle().stroke(.white, lineWidth: 4)
                                }
                                .shadow(radius: 7)
                            Spacer()
                            
                            Image("pig")
                                .scaleEffect(0.30)
                                .frame(width:100, height: 100)
                                .scaledToFit()
                                .clipShape(Circle())
                                .overlay {
                                    Circle().stroke(.white, lineWidth: 4)
                                }
                                .shadow(radius: 7)
                            Spacer()
                            
                            Image("prep7")
                                .scaleEffect(0.25)
                                .frame(width:100, height: 100)
                                .scaledToFit()
                                .clipShape(Circle())
                                .overlay {
                                    Circle().stroke(.white, lineWidth: 4)
                                }
                                .shadow(radius: 7)
                            Spacer()
                            
                            
                        }
                        HStack(alignment: .center){
                            Spacer()
                            Text("Prepos 4")
                                .font(.title2)
                                .fontWeight(.semibold).padding()
                            Spacer()
                            Text("Prepos 5")
                                .font(.title2)
                                .fontWeight(.semibold)
                                .multilineTextAlignment(.center)
                                .padding()
                            Spacer()
                            Text("Prepos 6")
                                .font(.title2)
                                .fontWeight(.semibold).padding()
                            Spacer()
                        }
                        HStack(alignment: .center){
                            Spacer()
                            Image("prep8")
                                .scaleEffect(0.20)
                                .frame(width:100, height: 100)
                                .scaledToFit()
                                .clipShape(Circle())
                                .overlay {
                                    Circle().stroke(.white, lineWidth: 4)
                                }
                                .shadow(radius: 7)
                            Spacer()
                            
                            Image("prep6")
                                .scaleEffect(0.20)
                                .frame(width:100, height: 100)
                                .scaledToFit()
                                .clipShape(Circle())
                                .overlay {
                                    Circle().stroke(.white, lineWidth: 4)
                                }
                                .shadow(radius: 7)
                            Spacer()
                            
                            Image("prep2")
                                .scaleEffect(0.20)
                                .frame(width:100, height: 100)
                                .scaledToFit()
                                .clipShape(Circle())
                                .overlay {
                                    Circle().stroke(.white, lineWidth: 4)
                                }
                                .shadow(radius: 7)
                            Spacer()
                            
                            
                        }
                        HStack(alignment: .center){
                            Spacer()
                            Text("Prepos 7")
                                .font(.title2)
                                .fontWeight(.semibold).padding()
                            Spacer()
                            Text("Prepos 8")
                                .font(.title2)
                                .fontWeight(.semibold)
                                .multilineTextAlignment(.center)
                                .padding()
                            Spacer()
                            Text("Prepos 9")
                                .font(.title2)
                                .fontWeight(.semibold).padding()
                            Spacer()
                        }
                        HStack(alignment: .center){
                            Image("prep4")
                                .scaleEffect(0.20)
                                .frame(width:100, height: 100)
                                .scaledToFit()
                                .clipShape(Circle())
                                .overlay {
                                    Circle().stroke(.white, lineWidth: 4)
                                }
                                .shadow(radius: 7).padding()
                            
                            
                            Image("earth")
                                .scaleEffect(0.20)
                                .frame(width:100, height: 100)
                                .scaledToFit()
                                .clipShape(Circle())
                                .overlay {
                                    Circle().stroke(.white, lineWidth: 4)
                                }
                                .shadow(radius: 7)
                            Spacer()
                            
                            
                            
                        }
                        HStack(alignment: .center){
                            Text("Prepos 10")
                                .font(.title2)
                                .fontWeight(.semibold).padding()
                            
                            Text("Prepos 11")
                                .font(.title2)
                                .fontWeight(.semibold)
                                .multilineTextAlignment(.center)
                                .padding()
                            Spacer()
                        }
                        
                    }
                    Spacer()
                    
                    
                    Group {
                        HStack{
                            Text("Verbos Comunes")
                                .font(.title)
                                .fontWeight(.bold)
                                .multilineTextAlignment(.center).padding()
                            Spacer()
                        }
                        
                        HStack(alignment: .center){
                            Spacer()
                            Image("com")
                                .scaleEffect(0.20)
                                .frame(width:100, height: 100)
                                .scaledToFit()
                                .clipShape(Circle())
                                .overlay {
                                    Circle().stroke(.white, lineWidth: 4)
                                }
                                .shadow(radius: 7)
                            Spacer()
                            
                            Image("running")
                                .scaleEffect(0.20)
                                .frame(width:100, height: 100)
                                .scaledToFit()
                                .clipShape(Circle())
                                .overlay {
                                    Circle().stroke(.white, lineWidth: 4)
                                }
                                .shadow(radius: 7)
                            Spacer()
                            
                            Image("earth4")
                                .scaleEffect(0.23)
                                .frame(width:100, height: 100)
                                .scaledToFit()
                                .clipShape(Circle())
                                .overlay {
                                    Circle().stroke(.white, lineWidth: 4)
                                }
                                .shadow(radius: 7)
                            Spacer()
                            
                            
                        }
                        
                        HStack(alignment: .center){
                            Spacer()
                            Text("Verbos 1")
                                .font(.title2)
                                .fontWeight(.semibold).padding()
                            Spacer()
                            Text("Verbos 2")
                                .font(.title2)
                                .fontWeight(.semibold)
                                .multilineTextAlignment(.center)
                                .padding()
                            Spacer()
                            Text("Verbos 3")
                                .font(.title2)
                                .fontWeight(.semibold).padding()
                            Spacer()
                        }
                    }
                    
                    Spacer()
                    
                    
                    Group{
                        HStack{
                            Text("Verbos Narrativos")
                                .font(.title)
                                .fontWeight(.bold)
                                .multilineTextAlignment(.center).padding()
                            Spacer()
                        }
                        
                        HStack(alignment: .center){
                            Image("lion")
                                .scaleEffect(0.25)
                                .frame(width:100, height: 100)
                                .scaledToFit()
                                .clipShape(Circle())
                                .overlay {
                                    Circle().stroke(.white, lineWidth: 4)
                                }
                                .shadow(radius: 7).padding()
                            
                            
                            Image("earth2")
                                .scaleEffect(0.25)
                                .frame(width:100, height: 100)
                                .scaledToFit()
                                .clipShape(Circle())
                                .overlay {
                                    Circle().stroke(.white, lineWidth: 4)
                                }
                                .shadow(radius: 7)
                            Spacer()
                            
                            
                            
                        }
                        HStack(alignment: .center){
                            Text("Narrativo 1")
                                .font(.title2)
                                .fontWeight(.semibold).padding()
                            
                            Text("Narrativo 2")
                                .font(.title2)
                                .fontWeight(.semibold)
                                .multilineTextAlignment(.center)
                                
                            Spacer()
                        }
                    }
                }
                
                
            }.navigationTitle("Aprende").navigationBarTitleDisplayMode(.automatic)
                

        }
    }
    
    struct AprenderView_Previews: PreviewProvider {
        static var previews: some View {
            AprenderView()
        }
    }
}
