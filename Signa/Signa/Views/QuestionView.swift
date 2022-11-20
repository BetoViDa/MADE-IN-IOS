//
//  QuestionView.swift
//  triviapi
//
//  Created by Victoria Lucero on 10/11/22.
//

import SwiftUI
import AVKit

struct QuestionView: View {
    @EnvironmentObject var triviaManager: TriviaManager
    
    var body: some View {
 
            VStack(spacing: 40){
                HStack{
                    title(text: "Trivia Game")
                    Spacer()
                    Text("\(triviaManager.index + 1) out of \(triviaManager.length)")
                        .foregroundColor(Color("AccentColor"))
                        .fontWeight(.heavy)
                  
                }
                ProgressBar(progress: triviaManager.progress)
                VStack(alignment: .leading, spacing: 20){
                    
                    if(triviaManager.trivia[triviaManager.index].fileType){ // true = image
                        // mostramos una imagen 
                        AsyncImage(url: URL(string: UrlDriveFiles + triviaManager.trivia[triviaManager.index].file)){ image in
                            image.resizable().frame(width: 200, height: 100)
                        } placeholder: {
                            ProgressView()
                        }
    
                    } else {
                        // mostramos un video
                        VideoPlayer(player: AVPlayer(url: URL(string: UrlDriveFiles + triviaManager.trivia[triviaManager.index].file)!))
                            .frame(width: 300, height: 120)
                    }

                    ForEach(triviaManager.answerChoices, id: \.id){
                        answer in AnswerRow(answer:answer)
                            .environmentObject(triviaManager)
                    }
                }
                
                Button{
                    triviaManager.goToNextQuestion()
                } label:{
                    PrimaryButtom(text: "Next", background: triviaManager.answerSelected ?  Color("AccentColor") : Color("adb5bd") )
                }
                .disabled(!triviaManager.answerSelected)
                  
            }.padding()
                .frame(maxWidth: .infinity, maxHeight: .infinity)
                .navigationBarHidden(true) /// esto es para que ya no salga el boton de back
        
    }
}

struct QuestionView_Previews: PreviewProvider {
    static var previews: some View {
        QuestionView()
            .environmentObject(TriviaManager())
    }
}
