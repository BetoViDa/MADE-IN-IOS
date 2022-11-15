//
//  QuestionView.swift
//  triviapi
//
//  Created by Victoria Lucero on 10/11/22.
//

import SwiftUI

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
                    Text(triviaManager.question)
                        .font(.system(size:20))
                        .bold()
                        .foregroundColor(.gray)
                    
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
