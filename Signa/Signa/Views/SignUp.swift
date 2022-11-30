//
//  SignUp.swift
//  loginswift
//
//  Created by Victoria Lucero on 09/11/22.
//

import SwiftUI
import UIKit


struct SignUp: View {
    
    struct Mensajes : Codable {
        var msj : String
        var ERROR : String
    }
    
    @State var username: String = ""
    @State var password: String = ""
    @State var email: String = ""
    @State var msjError: String = ""
    @State var msjErrorMail: String = ""
    @State var msjErrorNombre: String = ""
    @State var msjErrorContra: String = ""
    @State var msjErrorSignUp: String = ""
    @State var msjErrorTyC: String = ""
    @State var showView: Bool = false
    
    @State private var popupTyC = false
    @State private var AcceptTyC = false
    @State private var popupAvisPriv = false
    
    @State var showBack: Bool = false
    
    
    func makePostRequest(){
        // si falta aglun campo mostramos un error
        if(username == "" || email == "" || password == ""){
            msjError = ("Faltan campos de llenar")
        }
        else{ // no hay error
            msjError = "" // si se mostraba un error, y ya no se cumple volvemos a ocultarlo
        }
        // checar si se cumple con un buen correo, username y constrasenia
        
        //-----checar que el email sea valido-----
        let emailRegEx = "[A-Z0-9a-z._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,64}" // expresion regular
        let emailPred = NSPredicate(format:"SELF MATCHES %@", emailRegEx)
        if(!emailPred.evaluate(with: email)){ // mail invalido
            msjErrorMail = "Email no válido"
        }
        else{// no hay error
            msjErrorMail = ""
        }
        //=======================================
        
        //---checamos que user este correcto------
        let userRegEx = "[A-Z0-9a-z_/]{3,16}"
        let userPred = NSPredicate(format:"SELF MATCHES %@", userRegEx)
        if(!userPred.evaluate(with: username)){ // username invalido
            msjErrorNombre = "Tu nombre debe contener entre 3 y 16 caracteres y solo usar letras, números, _, /"
        }
        else{
            msjErrorNombre = ""
        }
        //========================================
        //--------Error con password--------------
        let passwordRegEx = "(?=.*[A-Za-z])(?=.*\\d)(?=.*[@$!%*#?&])[A-Za-z\\d@$!%*#?&]{8,}"
        //Minimum eight characters, at least one letter, one number and one special character:
        let passwordPred = NSPredicate(format:"SELF MATCHES %@", passwordRegEx)
        if(!passwordPred.evaluate(with: password)){
            msjErrorContra = "Mínimo 8 caracteres, una letra, un número, y un caracter especial. Solo se aceptan (@$!%*#?&)"
        }
        else{
            msjErrorContra = ""
        }
        
        //-----------Si no se aceptan los TyC---------------
        if (!AcceptTyC){
            msjErrorTyC = "Debes aceptar los Términos y Condiciones"
        } else {
            msjErrorTyC = ""
        }
        //===============================================
        
        //--------si hay error no continuamos----------
        if(msjError != "" || msjErrorMail != "" || msjErrorContra != "" || msjErrorNombre != "" || msjErrorTyC != ""){ // si se encontro un error
            print("Error por credenciales invalidas") // mostramos un error en consola
            return // no continuamos
        }
        //===============================================
        
        
        //--------------API--------------------------------
        guard let url = URL(string: APIURL + "/user/signup") else{
            return
        }//ponemos el url de la api en una variable string
        let body: [String:AnyHashable] = [
            "username" : username,
            "email": email,
            "password": password
        ]
        var request = URLRequest(url:url)//lo convertimos en una request para poder poner que es post y un body
        
        request.httpMethod = "POST"//ponemos su metodo como post
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = try? JSONSerialization.data(withJSONObject: body, options: .fragmentsAllowed)//ponemos el body con los datos en el request
        
        //creeamos la task pasandole el request
        let task = URLSession.shared.dataTask(with: request) {data, _, error in
            guard let data = data, error == nil else{
                return
            }
            do {
                
                let response = try JSONDecoder().decode(Mensajes.self, from: data)
                
                if (response.ERROR == "si"){
                    //MOSTRAR MENSAJE DE ERROR EN ROJO
                    msjErrorSignUp = response.msj
                    print(response.msj)
                } else {
                    //ME MANDARA A LOGIN
                    print(response.msj)
                    showBack = true
                    showView = true
                }
            } catch {
                print(error)
            }
        }
        task.resume()
    }
    
    
    var body: some View {
        ZStack{
            NavigationView{
                VStack{
                    Image("logoSigna").resizable().frame(width: 300, height:200)

                    VStack{
                        NavigationLink(destination: Login(), isActive: $showView){
                            Text("")
                        }
                        Text("\(msjErrorSignUp)")
                        Text("\(msjError)").font(.system(size: 9))
            
                        TextField("Usuario", text: $username).padding().background(Capsule()
                            .strokeBorder(Color.gray,lineWidth: 0.8)
                            .background(Color.white)
                            .clipped()).cornerRadius(10.0).padding(.horizontal,30.0)
                        Text("\(msjErrorNombre)").font(.system(size: 9))
                        TextField("Correo", text: $email).padding().background(Capsule()
                            .strokeBorder(Color.gray,lineWidth: 0.8)
                            .background(Color.white)
                            .clipped()).cornerRadius(5.0).padding(.horizontal,30.0)
                        Text("\(msjErrorMail)").font(.system(size: 9))
                        SecureField("Contraseña", text: $password).padding().background(Capsule()
                            .strokeBorder(Color.gray,lineWidth: 0.8)
                            .background(Color.white)
                            .clipped()).cornerRadius(5.0).padding(.horizontal,30.0)
                        Text("\(msjErrorContra)")
                            .font(.system(size: 9))
                        //Spacer()
                        Button("Registrate"){
                            makePostRequest()
                        }.buttonStyle(.borderedProminent).buttonBorderShape(.capsule).tint(Color.accentColor).foregroundColor(.white).controlSize(.large).fontWeight(.bold).font(.system(size:17, weight: .bold, design: .rounded))
                    }
                    HStack{
                        Button (action : {
                            popupTyC = true
                        }){
                            Text("Términos y Condiciones")
                                .foregroundColor(.blue)
                                .font(.system(size: 15))
                                
                        }
                        Text("|")
                            .foregroundColor(Color("adb5bd"))
                            .font(.system(size: 15))
                            .padding(.horizontal,2)
                       
                        Button (action : {
                            popupAvisPriv = true
                        }){
                            Text("Aviso de Privacidad")
                                .foregroundColor(.blue)
                                .font(.system(size: 15))

                            
                        }
                    }.padding(.all)
                   
                    Text("\(msjErrorTyC)").font(.system(size: 9))
                }
                
            }.navigationBarBackButtonHidden(showBack)
        }
        if popupTyC {
            VStack(){
                Text("Términos y Condiciones")
                    .font(.title2)
                    .padding(.top)
                ScrollView(.vertical){
                    Text("1. CONDICIONES GENERALES Y SU ACEPTACIÓN. Hola, bienvenidos a SIGNA Para nosotros es importante que usted esté enterado de los términos y condiciones antes de realizar alguna operación dentro de la aplicación. El uso de esta aplicación móvil llamada SIGNA da acceso a una gran variedad de conocimiento y archivos de enseñanza, así como información sobre el estatus de los usuarios dentro de un grupo, el cual se encuentra sujeto a los términos y condiciones de este acuerdo. SIGNA se reserva el derecho de modificar, cambiar, agregar o de quitar estos términos y condiciones en cualquier momento. Todos los archivos que son ofrecidos por nuestro app pudieran ser creadas, cobradas, enviadas o presentadas por una aplicación de un tercero y en tal caso estarían sujetas a sus propios Términos y Condiciones. Al iniciar el uso de la aplicación SIGNA, se presume que usted ha leído y consentido estos Términos y Condiciones de Uso. Al utilizar esta aplicación electrónicamente, usted reconoce que ha leído y aceptado sujetarse por estos términos y condiciones en toda su extensión y con todo su alcance legal. 2. OBJETO. Los Términos regulan la prestación del Servicio por parte de SIGNA y la utilización del Servicio por parte de los Usuarios. SIGNA se reserva el derecho a modificar unilateralmente, en cualquier momento y sin aviso previo, la prestación y configuración del Servicio, así como las condiciones requeridas para utilizar la aplicación. Revise estos términos y condiciones periódicamente para enterarse de cualesquier cambios, sin responsabilidad alguna para SIGNA el uso continuo de esta aplicación después de la publicación de algún cambio en estos Términos y Condiciones de Uso indica que el Usuario acepta dichos cambios sin reserva alguna. 3. SERVICIO. El servicio comprende las prestaciones de difusión de información, gestiones permitidas entre el Usuario y la aplicación, mensajes, archivos de imagen, videos y, en general, cualquier clase de material suministrado por SIGNA, quien no se encuentra comprometido a ninguna organización política o gubernamental. Para efectos de las presentes reglas de uso del app, se considerará usuario al: (i) público en general y/o (ii) cliente de SIGNA que haya generado un perfil de usuario, en el caso aplicable, o (iii) quien realice transacciones o consuma servicios a través de nuestro portal y/o antes de contratar alguno de nuestros servicios a través del mismo. El Usuario acepta plena e incondicionalmente tanto las reglas de uso de la aplicación, como el Aviso de Privacidad de SIGNA (conjuntamente, el “Aviso Legal”), publicados en nuestro portal. El Usuario reconoce y acepta plenamente que mediante el uso de la aplicación ha divulgado su personalidad legal con información completa, veraz, plena y sin que medie engaño o algún vicio del consentimiento. Así mismo, el Usuario reconoce que cuenta con plena capacidad legal para obligarse frente a terceros sin limitación alguna, y que no obra en beneficio de algún tercero beneficiario no divulgado, y que todas las actividades llevadas a cabo a través de la aplicación SIGNA las realiza con recursos de procedencia lícita y para fines lícitos. Lo anterior es aplicable en general para quien de alguna forma contrate o utilice servicios, realice cambios o consuma servicios a través de dicha aplicación. El Usuario reconoce plenamente las disposiciones aplicables de la legislación Mexicana en materia de comercio electrónico, uso de tecnología para identidad de partes contratantes ya sea mediante el uso de alguna firma electrónica o el intercambio de mensajes de datos, admitiendo así su validez legal e idoneidad como admisibles en materia de prueba en cualquier proceso judicial o administrativo en México. El Aviso Legal tiene carácter de obligatorio y vinculante para todos los Usuarios. En caso de que el Usuario no esté de acuerdo con el Aviso Legal, en todo o en parte, deberá abstenerse de utilizar, operar, visitar la aplicación de SIGNA. CONDICIONES DE ACCESO Y UTILIZACIÓN DEL SERVICIO. 3.1. Carácter gratuito del Servicio y Registro para la utilización del Servicio. La prestación del servicio por parte de SIGNA tiene carácter gratuito para los usuarios. No se exige la previa suscripción o registro de usuarios mediante cualquier método de pago. 3.2. Obligación de hacer un uso correcto del Servicio. El usuario se compromete a utilizar el Servicio de conformidad con la ley, estos Términos, así como de acuerdo con la moral y las buenas costumbres y el orden público. El Usuario se obliga de abstenerse de utilizar el Servicio con fines o efectos ilícitos, lesivos de los derechos e intereses de terceros o que de cualquier forma puedan dañar, inutilizar, sobrecargar o deteriorar el Servicio o impedir la utilización normal o disfrute del Servicio por parte de los Usuarios. Sin limitar la general de lo anterior, el Usuario se compromete a no hacer lo siguiente: Usar la aplicación en relación con la comisión de delitos patrimoniales o de cualquier otro tipo, en particular en materia de antilavado de dinero y anticorrupción. Usar la aplicación en relación con cartas en cadena, correo electrónico publicitario, correo electrónico de publicidad indeseada, ni ningún duplicado ni mensajes no solicitados, comerciales o de otra índole. Recopilar, compilar ni diseminar información acerca de terceros, incluyendo las direcciones de correo electrónico o datos personales, sin consentimiento del titular de la información o los datos. Crear una identidad falsa o una dirección de correo electrónico o encabezamiento falsificado, ni intentar de alguna manera engañar a otras personas sobre la identidad del remitente o el origen de un mensaje. Transmitir a través o hacia la aplicación materiales ilegales, hostigantes, difamatorios, abusivos, amenazantes, perjudiciales, vulgares, obscenos, ofensivos o de índole censurable. Transmitir algún material que pudiera infringir los derechos de propiedad intelectual u otros derechos de terceros, incluyendo y sin limitaciones, marcas comerciales, secretos comerciales o derechos de autor. Transmitir algún material que contenga virus, caballos de troya, gusanos, bombas de tiempo, programas de cancelación, ni ningún otro programa perjudicial o nocivo. Usar la aplicación para infringir alguna ley pertinente que restrinja la exportación o importación de datos, software o algún otro tipo de contenido. Interferir en, o perturbar, el funcionamiento de las redes conectadas con la aplicación de SIGNA o infringir las normas, políticas, reglas o procedimientos de tales redes. Obtener o intentar obtener acceso no autorizado al portal y la aplicación de SIGNA u otras cuentas, sistemas computacionales o redes conectadas con la aplicación de SIGNA, por medio de la búsqueda u obtención ilegal de contraseñas ni por ningún otro medio. Interferir en el uso de la aplicación por parte de algún tercero. Usar la aplicación de alguna manera no ética o de forma ilícita. Usar la aplicación para promocionar negocios en beneficio de alguna empresa o servicio de la competencia. Queda expresamente prohibido: (i) utilizar la aplicación y/o los Servicios para propósitos ilegales, inmorales, obscenos o prohibidos por la costumbre y la legislación aplicable y/o por el Aviso Legal; (ii) provocar modificaciones, alteraciones y/o supresiones, realizados por medios electrónicos o de cualquier otra forma, empleando recursos lícitos o ilícitos, que puedan interferir en la administración u operación de la aplicación y/o los Servicios prestados por SIGNA. El Usuario será responsable de los daños y perjuicios que se causen a SIGNA derivado de sus actos o de aquellos que provengan de sus funcionarios, empleados, agentes, dependientes, colaboradores y/o persona física o moral asociada, subsidiaria y/o filial. 3.3. Obtención de los Contenidos. El usuario deberá abstenerse de obtener e incluso de intentar obtener el contenido de la aplicación empleando para ello medio o procedimientos distintos de los que, según los casos, se hayan puesto a su disposición a este efecto o se hayan indicado a este efecto en la aplicación donde se encuentran los contenidos o, en general, de los que se empleen habitualmente en Internet a este efecto siempre que no entrañen un riesgo de daño o inutilización del Servicio. 3.4. Responsabilidad por daños y perjuicios. El usuario responderá de los daños y perjuicios de cualquier naturaleza que SIGNA pueda sufrir, directa o indirectamente, como consecuencia del incumplimiento de cualquiera de las obligaciones derivadas de los Términos y Condiciones de Uso y el Aviso Legal, o de la ley en relación con la utilización del Servicio. Es posible que la aplicación de SIGNA contenga enlaces a sitios, recursos o patrocinadores de terceros. La existencia de enlaces a y desde la aplicación a sitios de terceros no constituye un patrocinio de parte de SIGNA de ningún sitio, recursos, patrocinadores o contenido de terceros y SIGNA no acepta ninguna responsabilidad, directa o indirectamente, por ninguno de esos sitios, recursos, patrocinadores o contenido. SIGNA no hace declaración alguna ni aprueba la precisión o confiabilidad de ningún consejo, opinión, declaración ni alguna otra información presentada o distribuida a través de la aplicación. El Usuario acepta que, al confiar en alguna de dichas opiniones, consejos, declaraciones o información, lo hace a riesgo propio. SIGNA y sus socios, accionistas, consejeros, empleados, colaboradores, asesores y agentes no se responsabilizan ni ofrecen garantías de ningún tipo con respecto a: (1) el contenido de la aplicación; (2) los materiales, software, funciones e información a las cuales se obtenga acceso por medio del software utilizado en la aplicación y la Plataforma o a lo cual se obtenga acceso a través de los mismos; (3) todo producto o servicio de terceros o enlaces a terceros en la aplicación; o (4) cualquier violación a la seguridad asociada con la transmisión de información sensible a través de la aplicación o algún sitio enlazado. SIGNA y sus socios no otorgan ninguna garantía explícita o implícita, incluidas y sin limitaciones, las de no contravención o violación de leyes o reglamentos, comerciabilidad o idoneidad para un determinado propósito. SIGNA no garantiza que las funciones contenidas en la aplicación o algún material o contenido de los mismos estarán libres de interrupciones o errores, que todos los defectos se corregirán, o que la aplicación o el servidor en el cual funcionan están libres de virus u otros componentes perjudiciales. SIGNA no acepta ninguna responsabilidad por pérdidas o daños (incluidos y sin limitaciones, pérdidas o daños indirectos, especiales, consecuenciales o directos) que resulten del uso de la aplicación, independientemente de si éstos ocurren a consecuencia de algún acto negligente u omisión. 4. UTILIZACIÓN DE LOS SERVICIOS Y DE LOS CONTENIDOS BAJO LA EXCLUSIVA RESPONSABILIDAD DEL USUARIO. El Usuario expresamente reconoce y acepta voluntariamente que el uso del Servicio y de los Términos tiene lugar, en todo caso, bajo su única y exclusiva responsabilidad. 5. NO LICENCIA. SIGNA cuenta con la titularidad y propiedad exclusiva de los derechos otorgados por las leyes vigentes y/o tratados internacionales inherentes a la propiedad intelectual, para todas las marcas, avisos comerciales, software y programas de computación en general, y demás figuras susceptibles de protección legal conforme a la Ley de la Propiedad Industrial y la Ley Federal del Derecho de Autor, con relación al portal, mediante los cuales promueva, comercialice y preste sus Servicios, incluyendo pero sin limitar: (i) la propiedad industrial sobre los títulos de registros de marcas y avisos comerciales otorgados por el Instituto Mexicano de la Propiedad Industrial; (ii) los derechos de autor respecto del programa(s) de computación, desarrollos de software, sistema(s) y/o sus derivados, otorgados por el Instituto Nacional de Derechos de Autor; y (iii) todos los desarrollos, know how, signos distintivos y/o bienes o derechos que le correspondan en el ámbito de la propiedad intelectual por derecho propio (la “Propiedad Intelectual”). SIGNA no concede ninguna licencia o autorización de uso de ninguna clase sobre la Propiedad Intelectual, salvo acuerdo expreso por escrito, por lo que el Usuario reconoce que: (i) no tiene derecho alguno sobre la Propiedad Intelectual, por lo que se obliga a respetar en todo momento los derechos que detenta SIGNA sobre ésta; (ii) no podrá modificar, alterar, suprimir, copiar o reproducir ya sea total o parcialmente, incluyendo pero sin limitar, el contenido informativo generado por SIGNA, la Propiedad Intelectual y/o cualquier indicación contenida en la aplicación. 6. DENEGACIÓN Y RETIRADA DEL ACCESO AL app Y/O SERVICIO. SIGNA se reserva el derecho a denegar o retirar el acceso al servicio, en cualquier momento y sin necesidad de aviso previo a los Usuarios. SIGNA podrá, sin previo aviso, suspender, desconectar, denegar o restringir su acceso: (a) durante un fallo técnico de la aplicación, o durante la modificación o mantenimiento del mismo; (b) si el usuario usa la aplicación e infraestructura de SIGNA de manera que viole estas reglas de uso o la relación de servicios respectiva; o (c) si el Usuario hace algo o deja de hacer algo que en la opinión de SIGNA pudiera tener como consecuencia el poner en peligro el funcionamiento o la integridad de clientes o la aplicación SIGNA 7. DURACIÓN Y TERMINACIÓN. La prestación del Servicio tiene una duración indefinida. No obstante, SIGNA está autorizada para dar por terminada o suspender la prestación del Servicio en cualquier momento y por cualquier causa. Cuando ello sea razonablemente posible, SIGNA advertirá previamente la terminación o suspensión de la prestación del Servicio. 8. JURISDICCIÓN. En caso de cualquier controversia relacionada con el Servicio, el Usuario expresamente acuerda en someterse a las leyes aplicables de los Estados Unidos Mexicanos (“México”), y el Usuario expresamente acuerda en someterse a la jurisdicción exclusiva de los tribunales competentes ubicados en la ciudad de Monterrey, Nuevo León, México para resolver cualquier controversia relacionada con el Servicio. Para cualquier sugerencia o propuesta escríbanos por correo electrónico a (info@SIGNA). Para nosotros es importante que usted esté enterado de los términos y condiciones antes de realizar alguna compra en nuestra tienda en línea. El uso de esta aplicación SIGNA da acceso a información sobre el lenguaje de señas mexicano, el cual se encuentra sujeto a los términos y condiciones de este acuerdo. SIGNA se reserva el derecho de modificar, cambiar, agregar o de quitar estos términos y condiciones en cualquier momento.")
                }.padding(.all)
                HStack{
                    Button(action: {
                        withAnimation {
                            AcceptTyC = true
                            popupTyC = false
                        }
                    }, label: {
                        Text("Acepto")
                    })
                    Button(action: {
                        withAnimation {
                            AcceptTyC = false
                            popupTyC = false
                        }
                    }, label: {
                        Text("Rechazar")
                    })
                }
            }.frame(maxHeight: .infinity, alignment: .topLeading)
        }
        if popupAvisPriv {
            VStack(){
                Text("Aviso de Privacidad")
                    .font(.title2)
                    .padding(.top)
                ScrollView(.vertical){
                    Text("A fin de dar cumplimiento con lo establecido en la Ley Federal de Protección de Datos Personales en Posesión de los Particulares, su Reglamento y Lineamientos aplicables (la “Ley”), Signa., sus filiales y/o subsidiarias, y/o sus partes relacionadas (“Signa”), con domicilio en Av. Eugenio Garza Sada 2501 Sur, Tecnológico, 64849 Monterrey, N.L., (el “Domicilio”), (la “App”), titular de los derechos de la app digital denominada “Signa” (la“Aplicación”) y demás plataformas presentes y futuras de su propiedad, y con correo electrónico de contacto info@signa.mx (el “Correo Electrónico”), pone a su disposición el presente: Aviso de Privacidad. Con la finalidad de dar un tratamiento legítimo, controlado e informado a sus datos personales, que actualmente nos proporcione o en el futuro y que obren en nuestras bases de datos, así como para garantizar su privacidad y su derecho a la autodeterminación informativa al proporcionarnos dichos datos, siendo Signa responsable del uso y protección de sus datos personales los cuales serán tratados con base en los principios de licitud, consentimiento, información, calidad, finalidad, lealtad, proporcionalidad y responsabilidad previstos en la Ley. Utilización de la Información. La información que usted nos provea a través del acceso, registro y creación de una cuenta en la App y/o correo electrónico, y/o llenado de formularios o encuestas físicas o electrónicas, en tiempo real o histórico, se procesará y ordenará, para que genere indicadores de datos, mismos que Signa podrá usar para tomar decisiones pertinentes a su negocio. Toda la información que sea recopilada se utilizará con fines estadísticos, de manera genérica y no personalizada, y se asocian con el crecimiento, mantenimiento y administración de Signa, respetando en todo momento su privacidad. Estos usos incluyen nuestras operaciones y administración internas, la comunicación con usted y el cumplimiento de las solicitudes de servicios y/o productos provistos por Signa, así como para mejorar, desarrollar, perfeccionar y, proporcionar los servicios de Signa, a través de sus partes relacionadas, filiales, o proveedores autorizados y/o socios comerciales, estableciendo las medidas adecuadas a fin de limitar el uso de la información recabada de usted, únicamente para fines legales y autorizados de conformidad con este Aviso, así como con las debidas medidas de confidencialidad y seguridad. Signa también podrá recabar su dirección de IP (Internet Protocol) para ayudar a diagnosticar problemas con el servidor de Signa y para administrar la App. Una dirección de IP es un número que se le asigna a su computadora cuando usa Internet. Su dirección de IP también es utilizada para ayudar a identificarle dentro de una sesión particular y para recolectar información demográfica general. Signa podrá hacer uso de tecnología “push” a través de la aplicación que Signa usa para enviar notificaciones con autorización previa del Usuario. Este medio de comunicación no tiene ningún tipo de acceso a otras funciones o información del equipo con el que se conecta la aplicación. La información puede incluir la URL de la que provienen (estén o no en la App), a qué URL acceden seguidamente (estén o no en la App), qué navegador están usando, así como también las páginas visitadas, las búsquedas realizadas, las publicaciones, preferencias comerciales, mensajes, etc. Si Usted al utilizar la App, transfiere o da acceso a Signa a datos personales de terceros, Usted declara y confirma que tiene implementadas las medidas de seguridad administrativas, técnicas y físicas que permitan proteger los datos personales contra daño, pérdida, alteración, destrucción o el uso, acceso o tratamiento no autorizado de conformidad con lo dispuesto en la Ley y se obliga a mantener, y que tiene a disposición de dichos terceros, un Aviso de Privacidad que cumpla con las leyes, normas y regulaciones aplicables. Usted será responsable de cumplir con las ya mencionadas, incluyendo la autorización expresa para divulgar, recopilar, intercambiar y usar dichos datos de terceros. 1. Datos Personales Solicitados. Signa, y/o las empresas controladoras de éste y/o empresas filiales y/o subsidiarias y/o partes relacionadas solicita y obtiene datos personales en general, así como datos personales considerados sensibles por la Ley (en lo sucesivo “Datos Personales Generales” y “Datos Personales Sensibles”, respectivamente; y de manera conjunta referidos como los “Datos Personales”) de las personas en adelante descritas. Los Datos Personales Sensibles que pudieran ser recabados por Signa constan de estado de salud e información genética y podrán ser solicitados por medios electrónicos o físicos, en el entendido de que toda información proporcionada en físico, será considerada y tratada como si se hubiera proporcionado y autorizado en la App, y por lo cual se regirá por el presente documento. Los Datos Personales Generales que serán recabados constan de información personal como nombre, correo electrónico, número teléfono, entre otros, que es incluida o podrá ser incluida en formatos, listados, bases de datos u otros medios físicos y/o electrónicos, según corresponda, a efecto de que Signa pueda proveer de los Servicios y dar de alta la cuenta correspondiente en la App y con la finalidad establecida en el presente Aviso de Privacidad. En todos los casos, la recolección de Datos Personales por parte de Signa es realizada de buena fe y para los fines aquí expuestos; por tal motivo, se presume que los datos proporcionados por sus titulares son apegados a la verdad y completos, por lo que son responsabilidad del titular que los proporciona. 2. Finalidades del Tratamiento de los Datos Personales. Los Datos Personales proporcionados a Signa a través de la app serán utilizados según se ha mencionado anteriormente, con la finalidad de: Realizar el procesamiento de datos que permita crear su cuenta en la App y prestarle servicios a través de la App. Crear una base de datos de usuarios, clientes y otros terceros con los que Signa pueda crear relaciones comerciales. Una vez cumplidas las finalidades del tratamiento de sus Datos Personales, y cuando no exista disposición legal que establezca lo contrario, Signa procederá a la cancelación, eliminación y/o destrucción de los Datos Personales recibidos, en los términos establecidos por la Ley. 3. Transferencia. TRANSFERENCIA DE LOS DATOS PERSONALES E INFORMACIÓN. Los Datos Personales a que se refiere este Aviso podrán ser transferidos a: (i) terceros relacionados y/o aliados comerciales, con la finalidad de engrandecer la propuesta de valor de Signa, así como ofrecerle, con base en sus necesidades, otros productos y servicios; (ii) autoridades judiciales, mexicanas y extranjeras, con la finalidad de dar cumplimiento a la Ley, legislación, notificaciones, requerimientos u oficios de carácter judicial; (iii) a proveedores de servicios de internet sobre la cual esté montada la infraestructura tecnológica de Signa; y/o (iv) a proveedores de servicios de soporte técnico de la App. En caso de realizar alguna transferencia de sus Datos Personales, en los que se requiera su consentimiento expreso, se lo informaremos a efecto de recabar el mismo. En todos los casos, Signa comunicará el presente Aviso de Privacidad a estos terceros y se asegurará a través de la firma de convenios y/o la adopción de otros documentos vinculantes, que dichos terceros mantengan las medidas de seguridad administrativas, técnicas y físicas necesarias para resguardar sus Datos Personales, así como que dichos terceros únicamente utilicen sus Datos Personales para las finalidades para los cuales fueron recabados. Asimismo, tanto el Cliente como responsable de recabar los Datos Personales y Signa que facilita a través de la app la recabación y procesamiento de los mismos, así como cualquier otra persona relacionada con Signa que tenga acceso a la información contenida en este Aviso de Privacidad, quedarán obligados a resguardarse bajo las mismas normas de seguridad y confidencialidad, y a no revelar ni hacer mal uso de la misma, o en caso contrario serán responsables de conformidad con las leyes aplicables. No obstante lo anterior, Signa no transferirá sus Datos Personales a terceros no relacionados con Signa, salvo en los casos antes citados y los previstos en la Ley, sin su consentimiento previo. 4. Medios y Procedimientos para el Ejercicio de los Derechos ARCO. Usted, como titular de los Datos Personales proporcionados a Signa podrá solicitar en cualquier momento, el ejercicio de sus derechos de acceso, rectificación, cancelación u oposición (los “Derechos ARCO”) al tratamiento de sus Datos Personales, consistentes en: (i) acceder a sus Datos Personales y a los detalles del tratamiento de los mismos; (ii) rectificar sus Datos Personales en caso de ser inexactos o incompletos; (iii) cancelar sus Datos Personales cuando considere que no se requieren para alguna de las finalidades señalados en este Aviso de Privacidad, estén siendo utilizados para finalidades no consentidas o haya finalizado su relación contractual o de servicio u otra con el Signa; y (iv) oponerse al tratamiento de sus Datos Personales para fines específicos. Para tal fin, usted deberá seguir el proceso de presentar su petición por escrito a Signa, o bien, enviar su petición al Correo Electrónico, según sea aplicable, la cual deberá contener, como mínimo, la siguiente información: (a) su nombre completo y domicilio, u otro medio idóneo para comunicarle la respuesta a su solicitud; (b) los documentos que acrediten su identidad o, en su caso, la de su representante legal; (c) la descripción clara y precisa de los Datos Personales respecto de los que se busca ejercer alguno de los derechos antes mencionados; y (d) cualquier otro elemento o información que facilite la localización de los Datos Personales, así como cualquier otro documento requerido por la regulación actual en el momento de presentar la solicitud. Usted también podrá solicitar al Correo Electrónico mayor información sobre el procedimiento para ejercer sus Derechos ARCO. La respuesta a su solicitud le será dada a conocer por Signa en los términos y plazos establecidos en la Ley. No obstante, usted podrá obtener más información acerca del estado que guarda su solicitud y del plazo de respuesta de la misma, contactando a Signa o enviando su petición al Correo Electrónico, donde además podrán atender cualquier aclaración o duda que pudiera tener respecto al tratamiento de sus Datos Personales y el ejercicio de sus Derechos ARCO. 5. Revocación del Consentimiento; Limitación del Uso y Divulgación de los Datos Personales. Usted también podrá revocar, en cualquier momento, el consentimiento que haya otorgado a Signa para el tratamiento de sus Datos Personales, así como solicitar que se limite el uso y divulgación de los mismos, siempre y cuando no lo impida una disposición legal. Para tal fin, usted deberá presentar su solicitud por escrito a Signa, o bien, enviar su solicitud al Correo Electrónico, según sea aplicable. Dicha solicitud deberá cumplir con los mismos requisitos mencionados en la Sección 4. anterior. La respuesta a su solicitud le será dada a conocer por Signa en los términos y plazos establecidos en la Ley. No obstante, usted podrá obtener más información acerca del estado que guarda su solicitud y del plazo de respuesta de la misma, contactando a Signa o enviando su petición al Correo Electrónico, donde además podrán atender cualquier aclaración o duda que pudiera tener respecto al tratamiento y estos derechos que le corresponden respecto a sus Datos Personales. En caso de que sus Datos Personales hubiesen sido remitidos con anterioridad a la fecha de revocación del consentimiento, y sigan siendo tratados por encargados de Signa, éste hará del conocimiento de éstos últimos dicha revocación, para que procedan a efectuar lo conducente. 6. Cambios al Aviso de Privacidad. Signa se reserva el derecho de modificar y/o actualizar este Aviso de Privacidad, en alguna o todas sus partes, a su entera discreción, en cuyo caso lo comunicará aquí mismo a través de su aplicación; y, según sea el caso particular de cada titular, a través de sus redes internas, o por medio de un aviso que se colocará en los medios habituales (físicos o electrónicos) de comunicación de Signa y en un lugar visible del Domicilio, o mediante un aviso por escrito dirigido a su correo electrónico, según sea legalmente requerido. 7. Forma Física, Digital, Electrónica o en Línea. La Partes acuerdan que la forma para perfeccionar el acuerdo de voluntades entre ellas podrá ser el de formato impreso, digital, electrónico o en línea, en donde bastará manifestar su voluntad por medio de su aceptación, así como proporcionar los datos personales, en la propio Aplicación de Signa sin requerir estampar la firma en documento alguno.El presente Aviso de Privacidad ha sido modificado el día 26 de Noviembre del 2022.")
                }.padding(.all)
                Button(action: {
                    withAnimation {
                        popupAvisPriv = false
                    }
                }, label: {
                    Text("Cerrar")
                })
            }.frame(maxHeight: .infinity, alignment: .topLeading)
        }
    }
    
}

struct SignUp_Previews: PreviewProvider {
    static var previews: some View {
        SignUp()
    }
}
