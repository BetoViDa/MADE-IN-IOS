
import SwiftUI
import WrappingHStack

struct AprenderView: View {
    @StateObject var triviaManager = TriviaManager()
    @State var showview: Bool = false
    var namestopicsfront = ["ABC 1", "ABC 2", "ABC 3", "Preposiciones 1","Preposiciones 2", "Preposiciones 3", "Preposiciones 4", "Preposiciones 5", "Preposiciones 6", "Preposiciones 7", "Preposiciones 8", "Preposiciones 9", "Preposiciones 10", "Preposiciones 11", "Comunes 1", "Comunes 2", "Comunes 3", "Narrativos 1", "Narrativos 2"]
    var namestopicsapi = ["letras1", "letras2", "letras3", "preposiciones1", "preposiciones2", "preposiciones3","preposiciones4", "preposiciones5", "preposiciones6", "preposiciones7", "preposiciones8","preposiciones9", "preposiciones10", "preposiciones11", "verboscomunes1", "verboscomunes2","verboscomunes3", "verbosnarrativos1", "verbosnarrativos2"]
    var imgs = ["abc","panda","earth3", "5", "karate", "prep", "prep3", "pig", "prep7", "prep8", "prep6", "prep2", "prep4", "earth", "com", "running", "earth4", "lion", "earth2"]
    
    var body: some View {
    
        NavigationView {
            ScrollView {
                VStack(alignment: .center) {
                    Group {
                        NavigationLink(destination: TriviaView().navigationBarBackButtonHidden(true)
                            .environmentObject(triviaManager), isActive: $showview){
                                Text("")
                        }
                        HStack{
                            Text("ABC")
                                .font(.title)
                                .fontWeight(.bold)
                                .multilineTextAlignment(.center).padding()
                            Spacer()
                        }           
                        HStack(alignment: .center){
                            ForEach((0...2), id: \.self){index in
                                Spacer()
                                VStack(alignment: .center){
                                    Button(action: {
                                        TriviaCategor = namestopicsapi[index]
                               
                                        Task.init{
                                            await triviaManager.fetchTrivia()
                                            showview = true
                                        }
                                    }){
                                        Image(imgs[index])
                                            .scaleEffect(0.18)
                                            .frame(width:100, height: 100)
                                            .scaledToFit()
                                            .clipShape(Circle())
                                            .overlay {
                                                Circle().stroke(.white, lineWidth: 4)
                                            }
                                            .shadow(radius: 7)
                                    }
                                    Text(namestopicsfront[index])
                                        .font(.title3)
                                        .fontWeight(.semibold).padding()
                                }
                                Spacer()
                            }
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
                        WrappingHStack(3...13, id:\.self){index in
                            Spacer()
                            Spacer()
                            VStack(alignment: .center){
                                Button(action: {
                                    TriviaCategor = namestopicsapi[index]
                                    
                                    Task.init{
                                        await triviaManager.fetchTrivia()
                                        showview = true
                                    }
                                }){
                                    Image(imgs[index])
                                        .scaleEffect(0.18)
                                        .frame(width:100, height: 100)
                                        .scaledToFit()
                                        .clipShape(Circle())
                                        .overlay {
                                            Circle().stroke(.white, lineWidth: 4)
                                        }
                                        .shadow(radius: 7)
                                }
                                Text(namestopicsfront[index])
                                    .font(.system(size: 13))
                                    .fontWeight(.semibold).padding()
                            }
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
                            ForEach((14...16), id: \.self){index in
                                Spacer()
                                VStack(alignment: .center){
                                    Button(action: {
                                        TriviaCategor = namestopicsapi[index]
                                        
                                        Task.init{
                                            await triviaManager.fetchTrivia()
                                            showview = true
                                        }
                                    }){
                                        Image(imgs[index])
                                            .scaleEffect(0.18)
                                            .frame(width:100, height: 100)
                                            .scaledToFit()
                                            .clipShape(Circle())
                                            .overlay {
                                                Circle().stroke(.white, lineWidth: 4)
                                            }
                                            .shadow(radius: 7)
                                    }
                                    Text(namestopicsfront[index])
                                        .font(.system(size: 15))
                                        .fontWeight(.semibold).padding()
                                }
                                Spacer()
                            }
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
                            ForEach((17...18), id: \.self){index in
                                Spacer()
                                VStack(alignment: .center){
                                    Button(action: {
                                        TriviaCategor = namestopicsapi[index]
                                       
                                        Task.init{
                                            await triviaManager.fetchTrivia()
                                            showview = true
                                        }
                                    }){
                                        Image(imgs[index])
                                            .scaleEffect(0.18)
                                            .frame(width:100, height: 100)
                                            .scaledToFit()
                                            .clipShape(Circle())
                                            .overlay {
                                                Circle().stroke(.white, lineWidth: 4)
                                            }
                                            .shadow(radius: 7)
                                    }
                                    Text(namestopicsfront[index])
                                        .font(.system(size: 15.5))
                                        .fontWeight(.semibold).padding()
                                }
                                Spacer()
                            }
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


