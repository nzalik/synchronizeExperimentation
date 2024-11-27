package travel2.init;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;
import edu.fudan.common.entity.TravelInfo;
import travel2.service.TravelService;
import java.util.Date;

/**
 * @author fdse
 */
@Component
public class InitData implements CommandLineRunner {

    @Autowired
    TravelService service;

    String zhiDa = "ZhiDa";
    String shanghai = "shanghai";
    String nanjing = "nanjing";
    String beijing = "beijing";

    @Override
    public void run(String... args)throws Exception{
        TravelInfo info = new TravelInfo();

        info.setTripId("Z1234");
        info.setTrainTypeName(zhiDa);
        info.setRouteId("0b23bd3e-876a-4af3-b920-c50a90c90b04");
        info.setStartStationName(shanghai);
        info.setStationsName(nanjing);
        info.setTerminalStationName(beijing);
        info.setStartTime("2013-05-04 09:51:52"); //NOSONAR
        info.setEndTime("2013-05-04 15:51:52"); //NOSONAR
        service.create(info,null);

        info.setTripId("Z1235");
        info.setTrainTypeName(zhiDa);
        info.setRouteId("9fc9c261-3263-4bfa-82f8-bb44e06b2f52");
        info.setStartStationName(shanghai);
        info.setStationsName(nanjing);
        info.setTerminalStationName(beijing);
        info.setStartTime("2013-05-04 11:31:52"); //NOSONAR
        info.setEndTime("2013-05-04 17:51:52"); //NOSONAR
        service.create(info,null);

        info.setTripId("Z1236");
        info.setTrainTypeName(zhiDa);
        info.setRouteId("d693a2c5-ef87-4a3c-bef8-600b43f62c68");
        info.setStartStationName(shanghai);
        info.setStationsName(nanjing);
        info.setTerminalStationName(beijing);
        info.setStartTime("2013-05-04 7:05:52"); //NOSONAR
        info.setEndTime("2013-05-04 12:51:52"); //NOSONAR
        service.create(info,null);

        info.setTripId("T1235");
        info.setTrainTypeName("TeKuai");
        info.setRouteId("20eb7122-3a11-423f-b10a-be0dc5bce7db");
        info.setStartStationName(shanghai);
        info.setStationsName(nanjing);
        info.setTerminalStationName(beijing);
        info.setStartTime("2013-05-04 08:31:52"); //NOSONAR
        info.setEndTime("2013-05-04 17:21:52"); //NOSONAR
        service.create(info,null);

        info.setTripId("K1345");
        info.setTrainTypeName("KuaiSu");
        info.setRouteId("1367db1f-461e-4ab7-87ad-2bcc05fd9cb7");
        info.setStartStationName(shanghai);
        info.setStationsName(nanjing);
        info.setTerminalStationName(beijing);
        info.setStartTime("2013-05-04 07:51:52"); //NOSONAR
        info.setEndTime("2013-05-04 19:59:52"); //NOSONAR
        service.create(info,null);


    info.setTripId("00001");
    info.setTrainTypeName("GaoTieTwo");
    info.setRouteId("26e51ea0-f6a9-4c86-a8ca-81f3fb2a47af");
    info.setStartStationName("shanghai");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("taiyuan");
    info.setStartTime("2013-05-04 09:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 11:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00002");
    info.setTrainTypeName("DongCheOne");
    info.setRouteId("969ac023-12ed-4c5b-a80e-d117b5409b42");
    info.setStartStationName("shanghai");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("nanjing");
    info.setStartTime("2013-05-04 10:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 12:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00003");
    info.setTrainTypeName("GaoTieOne");
    info.setRouteId("a25a0971-6613-4788-a8eb-871c7d92724d");
    info.setStartStationName("shanghai");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("wuxi");
    info.setStartTime("2013-05-04 11:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 13:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00004");
    info.setTrainTypeName("GaoTieTwo");
    info.setRouteId("44ade071-6cd1-47eb-9038-89e28fae9314");
    info.setStartStationName("shanghai");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("suzhou");
    info.setStartTime("2013-05-04 12:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 14:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00005");
    info.setTrainTypeName("DongCheOne");
    info.setRouteId("bc9448f5-1121-4f18-9b0d-b248f46ddca6");
    info.setStartStationName("shanghai");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("shanghaihongqiao");
    info.setStartTime("2013-05-04 13:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 15:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00006");
    info.setTrainTypeName("GaoTieOne");
    info.setRouteId("dc65282d-affc-471f-8996-84e681e23a1a");
    info.setStartStationName("shanghai");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("beijing");
    info.setStartTime("2013-05-04 14:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 16:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00007");
    info.setTrainTypeName("GaoTieTwo");
    info.setRouteId("33ca384e-d098-4c21-8700-6347a5847299");
    info.setStartStationName("shanghai");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("shijiazhuang");
    info.setStartTime("2013-05-04 15:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 17:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00008");
    info.setTrainTypeName("DongCheOne");
    info.setRouteId("fed9e5cc-6f65-4fa8-8037-549204501c78");
    info.setStartStationName("shanghai");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("xuzhou");
    info.setStartTime("2013-05-04 16:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 18:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00009");
    info.setTrainTypeName("GaoTieOne");
    info.setRouteId("6aaae3c4-a9a1-4ac3-89dd-f3963407d27c");
    info.setStartStationName("shanghai");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("jinan");
    info.setStartTime("2013-05-04 17:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 19:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00010");
    info.setTrainTypeName("GaoTieTwo");
    info.setRouteId("90dd0f47-f06e-4f3e-8c15-16bb142dbeb1");
    info.setStartStationName("shanghai");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("hangzhou");
    info.setStartTime("2013-05-04 18:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 20:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00011");
    info.setTrainTypeName("DongCheOne");
    info.setRouteId("9d7e73cf-b2bf-450e-a5eb-1750fd8bb175");
    info.setStartStationName("shanghai");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("jiaxingnan");
    info.setStartTime("2013-05-04 19:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 21:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00012");
    info.setTrainTypeName("GaoTieOne");
    info.setRouteId("d88aea9d-637a-4389-912b-9b75d420ba8e");
    info.setStartStationName("shanghai");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("zhenjiang");
    info.setStartTime("2013-05-04 08:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 10:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00013");
    info.setTrainTypeName("GaoTieTwo");
    info.setRouteId("55fb52a1-5995-4528-94aa-919ee58de58c");
    info.setStartStationName("taiyuan");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("shanghai");
    info.setStartTime("2013-05-04 09:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 11:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00014");
    info.setTrainTypeName("DongCheOne");
    info.setRouteId("0ef35cf4-5b8f-480c-b350-4aff440624a9");
    info.setStartStationName("taiyuan");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("nanjing");
    info.setStartTime("2013-05-04 10:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 12:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00015");
    info.setTrainTypeName("GaoTieOne");
    info.setRouteId("6bf4b49d-5b80-438d-a605-b9329a8aa50b");
    info.setStartStationName("taiyuan");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("wuxi");
    info.setStartTime("2013-05-04 11:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 13:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00016");
    info.setTrainTypeName("GaoTieTwo");
    info.setRouteId("ba6045ab-e5eb-4c40-92d4-4330408514af");
    info.setStartStationName("taiyuan");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("suzhou");
    info.setStartTime("2013-05-04 12:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 14:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00017");
    info.setTrainTypeName("DongCheOne");
    info.setRouteId("c3fbe02b-ca65-4e02-b9ac-a933a0a6584a");
    info.setStartStationName("taiyuan");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("shanghaihongqiao");
    info.setStartTime("2013-05-04 13:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 15:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00018");
    info.setTrainTypeName("GaoTieOne");
    info.setRouteId("636acb82-4623-4f56-96e1-00180e8592b8");
    info.setStartStationName("taiyuan");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("beijing");
    info.setStartTime("2013-05-04 14:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 16:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00019");
    info.setTrainTypeName("GaoTieTwo");
    info.setRouteId("7677e67a-359a-4c53-b5ef-e34bda2e0043");
    info.setStartStationName("taiyuan");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("shijiazhuang");
    info.setStartTime("2013-05-04 15:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 17:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00020");
    info.setTrainTypeName("DongCheOne");
    info.setRouteId("727310f1-b00f-43e3-b0cd-2c9457cc7e5d");
    info.setStartStationName("taiyuan");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("xuzhou");
    info.setStartTime("2013-05-04 16:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 18:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00021");
    info.setTrainTypeName("GaoTieOne");
    info.setRouteId("e6803444-c8b1-48ce-b46e-8e41e46f01d7");
    info.setStartStationName("taiyuan");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("jinan");
    info.setStartTime("2013-05-04 17:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 19:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00022");
    info.setTrainTypeName("GaoTieTwo");
    info.setRouteId("02e89150-b89b-4e45-816f-41a0dd87b3b5");
    info.setStartStationName("taiyuan");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("hangzhou");
    info.setStartTime("2013-05-04 18:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 20:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00023");
    info.setTrainTypeName("DongCheOne");
    info.setRouteId("a7a1b42a-ad37-42ef-9a98-5657ed317285");
    info.setStartStationName("taiyuan");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("jiaxingnan");
    info.setStartTime("2013-05-04 19:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 21:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00024");
    info.setTrainTypeName("GaoTieOne");
    info.setRouteId("739ae845-90b2-4ff8-ad75-f02b2310871b");
    info.setStartStationName("taiyuan");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("zhenjiang");
    info.setStartTime("2013-05-04 08:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 10:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00025");
    info.setTrainTypeName("GaoTieTwo");
    info.setRouteId("4a203dd1-7a59-4b1f-b773-7285cb3302b6");
    info.setStartStationName("nanjing");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("shanghai");
    info.setStartTime("2013-05-04 09:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 11:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00026");
    info.setTrainTypeName("DongCheOne");
    info.setRouteId("b5579202-041f-4339-8385-25616b57af9e");
    info.setStartStationName("nanjing");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("taiyuan");
    info.setStartTime("2013-05-04 10:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 12:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00027");
    info.setTrainTypeName("GaoTieOne");
    info.setRouteId("cd4ff30f-79b9-46ab-8aeb-bd60db9a5e56");
    info.setStartStationName("nanjing");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("wuxi");
    info.setStartTime("2013-05-04 11:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 13:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00028");
    info.setTrainTypeName("GaoTieTwo");
    info.setRouteId("52a91672-90e2-4535-8bbe-c3137d88c932");
    info.setStartStationName("nanjing");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("suzhou");
    info.setStartTime("2013-05-04 12:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 14:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00029");
    info.setTrainTypeName("DongCheOne");
    info.setRouteId("40cf5027-2a2f-42df-b168-379aaac3e1ca");
    info.setStartStationName("nanjing");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("shanghaihongqiao");
    info.setStartTime("2013-05-04 13:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 15:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00030");
    info.setTrainTypeName("GaoTieOne");
    info.setRouteId("61f860e8-235e-4dc4-800a-684f188846ab");
    info.setStartStationName("nanjing");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("beijing");
    info.setStartTime("2013-05-04 14:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 16:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00031");
    info.setTrainTypeName("GaoTieTwo");
    info.setRouteId("9c4b7526-24dc-40fb-b3b4-0a6820f37182");
    info.setStartStationName("nanjing");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("shijiazhuang");
    info.setStartTime("2013-05-04 15:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 17:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00032");
    info.setTrainTypeName("DongCheOne");
    info.setRouteId("745d6764-e7fe-4cab-8b0a-e9594de6ad5e");
    info.setStartStationName("nanjing");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("xuzhou");
    info.setStartTime("2013-05-04 16:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 18:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00033");
    info.setTrainTypeName("GaoTieOne");
    info.setRouteId("ce2fb311-7c57-4e68-9cc0-c97b1c30d5c7");
    info.setStartStationName("nanjing");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("jinan");
    info.setStartTime("2013-05-04 17:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 19:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00034");
    info.setTrainTypeName("GaoTieTwo");
    info.setRouteId("6b0045aa-368b-4ec4-8da2-2b266ea14a74");
    info.setStartStationName("nanjing");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("hangzhou");
    info.setStartTime("2013-05-04 18:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 20:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00035");
    info.setTrainTypeName("DongCheOne");
    info.setRouteId("435bbe03-dc4c-444b-b56f-58483c4390bb");
    info.setStartStationName("nanjing");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("jiaxingnan");
    info.setStartTime("2013-05-04 19:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 21:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00036");
    info.setTrainTypeName("GaoTieOne");
    info.setRouteId("e76025ed-6da6-40ea-8eed-03d81368082b");
    info.setStartStationName("nanjing");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("zhenjiang");
    info.setStartTime("2013-05-04 08:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 10:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00037");
    info.setTrainTypeName("GaoTieTwo");
    info.setRouteId("786f0de4-20a7-490e-9375-6d30534833bd");
    info.setStartStationName("wuxi");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("shanghai");
    info.setStartTime("2013-05-04 09:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 11:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00038");
    info.setTrainTypeName("DongCheOne");
    info.setRouteId("791a068e-8265-44ce-b7ed-22103d7d60b3");
    info.setStartStationName("wuxi");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("taiyuan");
    info.setStartTime("2013-05-04 10:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 12:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00039");
    info.setTrainTypeName("GaoTieOne");
    info.setRouteId("89ef3a41-55f7-453b-be5e-43fd031a71e4");
    info.setStartStationName("wuxi");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("nanjing");
    info.setStartTime("2013-05-04 11:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 13:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00040");
    info.setTrainTypeName("GaoTieTwo");
    info.setRouteId("144c1088-88e6-4bc3-81ca-5bc1ca09cb89");
    info.setStartStationName("wuxi");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("suzhou");
    info.setStartTime("2013-05-04 12:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 14:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00041");
    info.setTrainTypeName("DongCheOne");
    info.setRouteId("c2fe04d8-4568-4203-99df-bd3b614c067e");
    info.setStartStationName("wuxi");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("shanghaihongqiao");
    info.setStartTime("2013-05-04 13:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 15:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00042");
    info.setTrainTypeName("GaoTieOne");
    info.setRouteId("1ed08557-b740-4e08-9df3-71793f02ce28");
    info.setStartStationName("wuxi");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("beijing");
    info.setStartTime("2013-05-04 14:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 16:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00043");
    info.setTrainTypeName("GaoTieTwo");
    info.setRouteId("1ff09d1d-4eb0-4e73-8361-98c2edf4d5ab");
    info.setStartStationName("wuxi");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("shijiazhuang");
    info.setStartTime("2013-05-04 15:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 17:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00044");
    info.setTrainTypeName("DongCheOne");
    info.setRouteId("63b98860-e755-4f7a-9484-f2fffb617689");
    info.setStartStationName("wuxi");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("xuzhou");
    info.setStartTime("2013-05-04 16:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 18:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00045");
    info.setTrainTypeName("GaoTieOne");
    info.setRouteId("c554f027-f887-4435-8c76-386ff385e4a6");
    info.setStartStationName("wuxi");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("jinan");
    info.setStartTime("2013-05-04 17:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 19:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00046");
    info.setTrainTypeName("GaoTieTwo");
    info.setRouteId("4a8ea889-1bbb-4fc4-8eba-84d7487194b8");
    info.setStartStationName("wuxi");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("hangzhou");
    info.setStartTime("2013-05-04 18:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 20:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00047");
    info.setTrainTypeName("DongCheOne");
    info.setRouteId("3fb310ea-861a-4945-9601-78753bd64a3b");
    info.setStartStationName("wuxi");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("jiaxingnan");
    info.setStartTime("2013-05-04 19:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 21:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00048");
    info.setTrainTypeName("GaoTieOne");
    info.setRouteId("093de207-cc6b-4be6-b2f3-3dfb4095f457");
    info.setStartStationName("wuxi");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("zhenjiang");
    info.setStartTime("2013-05-04 08:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 10:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00049");
    info.setTrainTypeName("GaoTieTwo");
    info.setRouteId("3cfe1cb3-dc9e-4d1d-a53c-7cf60091b3f1");
    info.setStartStationName("suzhou");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("shanghai");
    info.setStartTime("2013-05-04 09:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 11:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00050");
    info.setTrainTypeName("DongCheOne");
    info.setRouteId("1321d287-04b5-4787-b255-472ef276bd3f");
    info.setStartStationName("suzhou");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("taiyuan");
    info.setStartTime("2013-05-04 10:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 12:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00051");
    info.setTrainTypeName("GaoTieOne");
    info.setRouteId("c02bcf4e-f500-45bf-a9f2-b02effffcfe0");
    info.setStartStationName("suzhou");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("nanjing");
    info.setStartTime("2013-05-04 11:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 13:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00052");
    info.setTrainTypeName("GaoTieTwo");
    info.setRouteId("90e071f9-63ab-4d9d-a2be-3c31050ff924");
    info.setStartStationName("suzhou");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("wuxi");
    info.setStartTime("2013-05-04 12:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 14:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00053");
    info.setTrainTypeName("DongCheOne");
    info.setRouteId("e22b31e2-7418-4337-a383-f3e4f36171e9");
    info.setStartStationName("suzhou");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("shanghaihongqiao");
    info.setStartTime("2013-05-04 13:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 15:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00054");
    info.setTrainTypeName("GaoTieOne");
    info.setRouteId("beb473f3-ed1f-45da-9bcb-f4ee61a25555");
    info.setStartStationName("suzhou");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("beijing");
    info.setStartTime("2013-05-04 14:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 16:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00055");
    info.setTrainTypeName("GaoTieTwo");
    info.setRouteId("5eda7ef8-72df-49c4-bf4e-0a850b244f2c");
    info.setStartStationName("suzhou");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("shijiazhuang");
    info.setStartTime("2013-05-04 15:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 17:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00056");
    info.setTrainTypeName("DongCheOne");
    info.setRouteId("53986be9-32a2-49be-ab8a-7a89c04df8d9");
    info.setStartStationName("suzhou");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("xuzhou");
    info.setStartTime("2013-05-04 16:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 18:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00057");
    info.setTrainTypeName("GaoTieOne");
    info.setRouteId("42dbdf08-a4b7-4744-942c-39cad64fe00c");
    info.setStartStationName("suzhou");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("jinan");
    info.setStartTime("2013-05-04 17:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 19:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00058");
    info.setTrainTypeName("GaoTieTwo");
    info.setRouteId("25656113-c68f-4b46-a1d0-8771666638ce");
    info.setStartStationName("suzhou");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("hangzhou");
    info.setStartTime("2013-05-04 18:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 20:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00059");
    info.setTrainTypeName("DongCheOne");
    info.setRouteId("d8262a4d-492f-40e0-b829-e88f55ddaaab");
    info.setStartStationName("suzhou");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("jiaxingnan");
    info.setStartTime("2013-05-04 19:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 21:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00060");
    info.setTrainTypeName("GaoTieOne");
    info.setRouteId("8c3057ea-4596-4b85-a0fd-a9578b703338");
    info.setStartStationName("suzhou");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("zhenjiang");
    info.setStartTime("2013-05-04 08:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 10:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00061");
    info.setTrainTypeName("GaoTieTwo");
    info.setRouteId("d4ec77a3-c4f6-43ad-b1fc-6e6ad3b2e150");
    info.setStartStationName("shanghaihongqiao");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("shanghai");
    info.setStartTime("2013-05-04 09:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 11:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00062");
    info.setTrainTypeName("DongCheOne");
    info.setRouteId("d802c19b-d255-4d2c-b1d5-9767c00b824e");
    info.setStartStationName("shanghaihongqiao");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("taiyuan");
    info.setStartTime("2013-05-04 10:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 12:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00063");
    info.setTrainTypeName("GaoTieOne");
    info.setRouteId("6fe104a2-510c-41ac-89f0-17a04433833d");
    info.setStartStationName("shanghaihongqiao");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("nanjing");
    info.setStartTime("2013-05-04 11:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 13:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00064");
    info.setTrainTypeName("GaoTieTwo");
    info.setRouteId("e6557d91-47b9-4f7d-9660-11c75299d20b");
    info.setStartStationName("shanghaihongqiao");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("wuxi");
    info.setStartTime("2013-05-04 12:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 14:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00065");
    info.setTrainTypeName("DongCheOne");
    info.setRouteId("5e5e33c3-98c4-4734-b432-e64ec4e96cd9");
    info.setStartStationName("shanghaihongqiao");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("suzhou");
    info.setStartTime("2013-05-04 13:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 15:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00066");
    info.setTrainTypeName("GaoTieOne");
    info.setRouteId("2f064764-b0bf-43a8-b856-7397b3a1ff92");
    info.setStartStationName("shanghaihongqiao");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("beijing");
    info.setStartTime("2013-05-04 14:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 16:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00067");
    info.setTrainTypeName("GaoTieTwo");
    info.setRouteId("f0afff61-9977-43e9-b995-9d7bc30db60e");
    info.setStartStationName("shanghaihongqiao");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("shijiazhuang");
    info.setStartTime("2013-05-04 15:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 17:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00068");
    info.setTrainTypeName("DongCheOne");
    info.setRouteId("46925dfe-b85d-4931-a5cb-87a84c3b842b");
    info.setStartStationName("shanghaihongqiao");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("xuzhou");
    info.setStartTime("2013-05-04 16:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 18:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00069");
    info.setTrainTypeName("GaoTieOne");
    info.setRouteId("cf56cc68-5e2a-4add-b3d4-b67a9996887e");
    info.setStartStationName("shanghaihongqiao");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("jinan");
    info.setStartTime("2013-05-04 17:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 19:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00070");
    info.setTrainTypeName("GaoTieTwo");
    info.setRouteId("31765968-0269-40bb-99ce-50b15411eb23");
    info.setStartStationName("shanghaihongqiao");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("hangzhou");
    info.setStartTime("2013-05-04 18:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 20:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00071");
    info.setTrainTypeName("DongCheOne");
    info.setRouteId("550406d4-44fe-4cb5-bad2-81c793b463e4");
    info.setStartStationName("shanghaihongqiao");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("jiaxingnan");
    info.setStartTime("2013-05-04 19:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 21:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00072");
    info.setTrainTypeName("GaoTieOne");
    info.setRouteId("866dd64f-8066-4e5d-8334-b3ef721ca0c7");
    info.setStartStationName("shanghaihongqiao");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("zhenjiang");
    info.setStartTime("2013-05-04 08:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 10:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00073");
    info.setTrainTypeName("GaoTieTwo");
    info.setRouteId("71ab79bd-e28c-47fc-a103-7b257c660dec");
    info.setStartStationName("beijing");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("shanghai");
    info.setStartTime("2013-05-04 09:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 11:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00074");
    info.setTrainTypeName("DongCheOne");
    info.setRouteId("766185f4-3970-452d-a4be-a3178cb5f7eb");
    info.setStartStationName("beijing");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("taiyuan");
    info.setStartTime("2013-05-04 10:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 12:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00075");
    info.setTrainTypeName("GaoTieOne");
    info.setRouteId("5b6c3456-d2d0-4b19-9ee1-f71428aeb9fe");
    info.setStartStationName("beijing");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("nanjing");
    info.setStartTime("2013-05-04 11:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 13:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00076");
    info.setTrainTypeName("GaoTieTwo");
    info.setRouteId("68bc33b7-e22f-475d-b3e2-17c374b55e2e");
    info.setStartStationName("beijing");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("wuxi");
    info.setStartTime("2013-05-04 12:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 14:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00077");
    info.setTrainTypeName("DongCheOne");
    info.setRouteId("5d716d44-cd5c-4f0d-b777-f78e223e00e7");
    info.setStartStationName("beijing");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("suzhou");
    info.setStartTime("2013-05-04 13:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 15:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00078");
    info.setTrainTypeName("GaoTieOne");
    info.setRouteId("3b697760-2c03-46a3-9a90-7a156c22c1cb");
    info.setStartStationName("beijing");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("shanghaihongqiao");
    info.setStartTime("2013-05-04 14:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 16:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00079");
    info.setTrainTypeName("GaoTieTwo");
    info.setRouteId("0efe10f2-21d4-477f-b4ff-8d9b843f9be4");
    info.setStartStationName("beijing");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("shijiazhuang");
    info.setStartTime("2013-05-04 15:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 17:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00080");
    info.setTrainTypeName("DongCheOne");
    info.setRouteId("68f5f6a1-d17d-4004-ac78-972a647d03ee");
    info.setStartStationName("beijing");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("xuzhou");
    info.setStartTime("2013-05-04 16:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 18:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00081");
    info.setTrainTypeName("GaoTieOne");
    info.setRouteId("71209ead-7016-4fd4-a079-c8cb2f1efc21");
    info.setStartStationName("beijing");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("jinan");
    info.setStartTime("2013-05-04 17:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 19:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00082");
    info.setTrainTypeName("GaoTieTwo");
    info.setRouteId("362a4abf-61c1-4405-932f-7c367a9f89c2");
    info.setStartStationName("beijing");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("hangzhou");
    info.setStartTime("2013-05-04 18:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 20:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00083");
    info.setTrainTypeName("DongCheOne");
    info.setRouteId("e9c23f65-efeb-41bb-9649-5e02f1f1a14c");
    info.setStartStationName("beijing");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("jiaxingnan");
    info.setStartTime("2013-05-04 19:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 21:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00084");
    info.setTrainTypeName("GaoTieOne");
    info.setRouteId("3a232644-6429-43df-9e8f-a09e999b32b7");
    info.setStartStationName("beijing");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("zhenjiang");
    info.setStartTime("2013-05-04 08:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 10:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00085");
    info.setTrainTypeName("GaoTieTwo");
    info.setRouteId("07b9260a-5681-4985-97dc-6e0e491c5b42");
    info.setStartStationName("shijiazhuang");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("shanghai");
    info.setStartTime("2013-05-04 09:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 11:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00086");
    info.setTrainTypeName("DongCheOne");
    info.setRouteId("b1db4548-f9a4-4544-a553-647f613b110d");
    info.setStartStationName("shijiazhuang");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("taiyuan");
    info.setStartTime("2013-05-04 10:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 12:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00087");
    info.setTrainTypeName("GaoTieOne");
    info.setRouteId("e5579afa-8f30-416f-86d6-74fca5a1e075");
    info.setStartStationName("shijiazhuang");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("nanjing");
    info.setStartTime("2013-05-04 11:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 13:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00088");
    info.setTrainTypeName("GaoTieTwo");
    info.setRouteId("716a5bab-9852-45da-bfd0-c00f3d87f062");
    info.setStartStationName("shijiazhuang");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("wuxi");
    info.setStartTime("2013-05-04 12:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 14:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00089");
    info.setTrainTypeName("DongCheOne");
    info.setRouteId("7b181d5d-f407-4887-9581-8d7c5d658c9a");
    info.setStartStationName("shijiazhuang");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("suzhou");
    info.setStartTime("2013-05-04 13:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 15:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00090");
    info.setTrainTypeName("GaoTieOne");
    info.setRouteId("5e0002c9-3e98-4d16-b939-2058e2fddc86");
    info.setStartStationName("shijiazhuang");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("shanghaihongqiao");
    info.setStartTime("2013-05-04 14:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 16:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00091");
    info.setTrainTypeName("GaoTieTwo");
    info.setRouteId("9a9dd6f3-698f-4ddf-8e76-86bb66e83f81");
    info.setStartStationName("shijiazhuang");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("beijing");
    info.setStartTime("2013-05-04 15:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 17:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00092");
    info.setTrainTypeName("DongCheOne");
    info.setRouteId("633335e2-88ef-463a-81fe-aad998090f26");
    info.setStartStationName("shijiazhuang");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("xuzhou");
    info.setStartTime("2013-05-04 16:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 18:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00093");
    info.setTrainTypeName("GaoTieOne");
    info.setRouteId("32ae1713-32c7-4350-836c-d65e51f37b2e");
    info.setStartStationName("shijiazhuang");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("jinan");
    info.setStartTime("2013-05-04 17:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 19:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00094");
    info.setTrainTypeName("GaoTieTwo");
    info.setRouteId("8e28af9b-a0c7-474a-8d44-21aff42fb65b");
    info.setStartStationName("shijiazhuang");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("hangzhou");
    info.setStartTime("2013-05-04 18:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 20:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00095");
    info.setTrainTypeName("DongCheOne");
    info.setRouteId("d75e5e37-cf1c-48d4-9903-9373070ff14f");
    info.setStartStationName("shijiazhuang");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("jiaxingnan");
    info.setStartTime("2013-05-04 19:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 21:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00096");
    info.setTrainTypeName("GaoTieOne");
    info.setRouteId("5ba8373d-015d-4731-a70b-5f6ab9910076");
    info.setStartStationName("shijiazhuang");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("zhenjiang");
    info.setStartTime("2013-05-04 08:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 10:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00097");
    info.setTrainTypeName("GaoTieTwo");
    info.setRouteId("524cdb4c-b6a6-4874-bed4-abf6010d06e2");
    info.setStartStationName("xuzhou");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("shanghai");
    info.setStartTime("2013-05-04 09:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 11:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00098");
    info.setTrainTypeName("DongCheOne");
    info.setRouteId("08fd121c-2f58-40e5-a057-a9361822faa3");
    info.setStartStationName("xuzhou");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("taiyuan");
    info.setStartTime("2013-05-04 10:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 12:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00099");
    info.setTrainTypeName("GaoTieOne");
    info.setRouteId("230558c3-a15c-4676-be51-ead1969dbf0c");
    info.setStartStationName("xuzhou");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("nanjing");
    info.setStartTime("2013-05-04 11:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 13:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00100");
    info.setTrainTypeName("GaoTieTwo");
    info.setRouteId("9c47bfde-4dce-4ca3-8233-6e072b926889");
    info.setStartStationName("xuzhou");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("wuxi");
    info.setStartTime("2013-05-04 12:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 14:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00101");
    info.setTrainTypeName("DongCheOne");
    info.setRouteId("c2cdfbe0-86e9-4772-b78c-2963148fe710");
    info.setStartStationName("xuzhou");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("suzhou");
    info.setStartTime("2013-05-04 13:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 15:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00102");
    info.setTrainTypeName("GaoTieOne");
    info.setRouteId("3da982f3-6514-4fc9-bd66-201f67916b99");
    info.setStartStationName("xuzhou");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("shanghaihongqiao");
    info.setStartTime("2013-05-04 14:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 16:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00103");
    info.setTrainTypeName("GaoTieTwo");
    info.setRouteId("90334b83-fac1-41a2-95ff-8c025d7e9f75");
    info.setStartStationName("xuzhou");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("beijing");
    info.setStartTime("2013-05-04 15:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 17:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00104");
    info.setTrainTypeName("DongCheOne");
    info.setRouteId("3af885a4-ebba-4758-8eea-80ae3487542a");
    info.setStartStationName("xuzhou");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("shijiazhuang");
    info.setStartTime("2013-05-04 16:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 18:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00105");
    info.setTrainTypeName("GaoTieOne");
    info.setRouteId("05d1322b-cae8-4cb6-9ad5-3a6ebf390d00");
    info.setStartStationName("xuzhou");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("jinan");
    info.setStartTime("2013-05-04 17:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 19:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00106");
    info.setTrainTypeName("GaoTieTwo");
    info.setRouteId("1f65c2c8-1ccf-42b9-bc9d-42747b2dd4f5");
    info.setStartStationName("xuzhou");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("hangzhou");
    info.setStartTime("2013-05-04 18:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 20:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00107");
    info.setTrainTypeName("DongCheOne");
    info.setRouteId("a7a56054-542c-4269-b9e7-6f24e5da03e6");
    info.setStartStationName("xuzhou");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("jiaxingnan");
    info.setStartTime("2013-05-04 19:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 21:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00108");
    info.setTrainTypeName("GaoTieOne");
    info.setRouteId("8b15a9c1-a779-4b0f-82ab-2d20dedfa532");
    info.setStartStationName("xuzhou");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("zhenjiang");
    info.setStartTime("2013-05-04 08:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 10:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00109");
    info.setTrainTypeName("GaoTieTwo");
    info.setRouteId("2cc1a710-ba6b-473f-824a-3aa2c7f7b436");
    info.setStartStationName("jinan");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("shanghai");
    info.setStartTime("2013-05-04 09:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 11:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00110");
    info.setTrainTypeName("DongCheOne");
    info.setRouteId("7c715732-5755-4eb2-adaf-b85e4adb9492");
    info.setStartStationName("jinan");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("taiyuan");
    info.setStartTime("2013-05-04 10:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 12:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00111");
    info.setTrainTypeName("GaoTieOne");
    info.setRouteId("e48b047f-a3d2-4da5-9601-ac6f8e8fb231");
    info.setStartStationName("jinan");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("nanjing");
    info.setStartTime("2013-05-04 11:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 13:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00112");
    info.setTrainTypeName("GaoTieTwo");
    info.setRouteId("c9f307f0-8d1d-49d3-a948-fa98548b8b4a");
    info.setStartStationName("jinan");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("wuxi");
    info.setStartTime("2013-05-04 12:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 14:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00113");
    info.setTrainTypeName("DongCheOne");
    info.setRouteId("d09b593e-27d2-44f8-88a9-091f733f73f7");
    info.setStartStationName("jinan");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("suzhou");
    info.setStartTime("2013-05-04 13:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 15:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00114");
    info.setTrainTypeName("GaoTieOne");
    info.setRouteId("cce9ebf6-5a84-451b-954b-e8723e6a83fb");
    info.setStartStationName("jinan");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("shanghaihongqiao");
    info.setStartTime("2013-05-04 14:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 16:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00115");
    info.setTrainTypeName("GaoTieTwo");
    info.setRouteId("f478086b-f8cb-4ae2-8e6f-6d02abd7c2c9");
    info.setStartStationName("jinan");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("beijing");
    info.setStartTime("2013-05-04 15:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 17:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00116");
    info.setTrainTypeName("DongCheOne");
    info.setRouteId("c68d1e08-bd8b-410b-9c07-45a52cc6b497");
    info.setStartStationName("jinan");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("shijiazhuang");
    info.setStartTime("2013-05-04 16:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 18:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00117");
    info.setTrainTypeName("GaoTieOne");
    info.setRouteId("b4263ba6-3e60-40c9-ba1c-6b97814d94d0");
    info.setStartStationName("jinan");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("xuzhou");
    info.setStartTime("2013-05-04 17:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 19:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00118");
    info.setTrainTypeName("GaoTieTwo");
    info.setRouteId("6b60137e-823f-49c4-baf5-307c66f1e598");
    info.setStartStationName("jinan");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("hangzhou");
    info.setStartTime("2013-05-04 18:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 20:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00119");
    info.setTrainTypeName("DongCheOne");
    info.setRouteId("fada27b1-79a1-4268-9eb4-b3e9c2a8983d");
    info.setStartStationName("jinan");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("jiaxingnan");
    info.setStartTime("2013-05-04 19:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 21:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00120");
    info.setTrainTypeName("GaoTieOne");
    info.setRouteId("5fbec9bd-ba55-4514-8e38-780254c2ad96");
    info.setStartStationName("jinan");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("zhenjiang");
    info.setStartTime("2013-05-04 08:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 10:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00121");
    info.setTrainTypeName("GaoTieTwo");
    info.setRouteId("06ecec0e-2bd8-4fff-9bfc-e928b46295b4");
    info.setStartStationName("hangzhou");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("shanghai");
    info.setStartTime("2013-05-04 09:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 11:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00122");
    info.setTrainTypeName("DongCheOne");
    info.setRouteId("40be9b4a-003f-4efb-92fc-89ed93d2a669");
    info.setStartStationName("hangzhou");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("taiyuan");
    info.setStartTime("2013-05-04 10:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 12:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00123");
    info.setTrainTypeName("GaoTieOne");
    info.setRouteId("7f48940f-36ce-4485-8fdc-46bdca418893");
    info.setStartStationName("hangzhou");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("nanjing");
    info.setStartTime("2013-05-04 11:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 13:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00124");
    info.setTrainTypeName("GaoTieTwo");
    info.setRouteId("c23ca677-69b5-475e-b3fb-787d00631da4");
    info.setStartStationName("hangzhou");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("wuxi");
    info.setStartTime("2013-05-04 12:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 14:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00125");
    info.setTrainTypeName("DongCheOne");
    info.setRouteId("2abfba6e-bbb2-4989-8fb5-8f7fb2efbaee");
    info.setStartStationName("hangzhou");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("suzhou");
    info.setStartTime("2013-05-04 13:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 15:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00126");
    info.setTrainTypeName("GaoTieOne");
    info.setRouteId("49bc67a7-eab0-448d-8b6b-680cb19fa075");
    info.setStartStationName("hangzhou");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("shanghaihongqiao");
    info.setStartTime("2013-05-04 14:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 16:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00127");
    info.setTrainTypeName("GaoTieTwo");
    info.setRouteId("a0a712b7-dbbb-4ad3-b4ca-506b356136ad");
    info.setStartStationName("hangzhou");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("beijing");
    info.setStartTime("2013-05-04 15:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 17:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00128");
    info.setTrainTypeName("DongCheOne");
    info.setRouteId("46101d16-46d4-405c-b085-44c9337801f9");
    info.setStartStationName("hangzhou");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("shijiazhuang");
    info.setStartTime("2013-05-04 16:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 18:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00129");
    info.setTrainTypeName("GaoTieOne");
    info.setRouteId("837e99cc-d71e-4595-86e2-d9beae565ff7");
    info.setStartStationName("hangzhou");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("xuzhou");
    info.setStartTime("2013-05-04 17:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 19:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00130");
    info.setTrainTypeName("GaoTieTwo");
    info.setRouteId("e31cc73e-a069-4952-be37-6f2619562f02");
    info.setStartStationName("hangzhou");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("jinan");
    info.setStartTime("2013-05-04 18:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 20:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00131");
    info.setTrainTypeName("DongCheOne");
    info.setRouteId("024cdc3c-ddb2-4001-95f4-77169eee8922");
    info.setStartStationName("hangzhou");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("jiaxingnan");
    info.setStartTime("2013-05-04 19:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 21:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00132");
    info.setTrainTypeName("GaoTieOne");
    info.setRouteId("24f58b2e-caef-4a1f-9ad0-540c690b0cb1");
    info.setStartStationName("hangzhou");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("zhenjiang");
    info.setStartTime("2013-05-04 08:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 10:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00133");
    info.setTrainTypeName("GaoTieTwo");
    info.setRouteId("25e455b6-0c30-4531-8511-57453180e4e9");
    info.setStartStationName("jiaxingnan");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("shanghai");
    info.setStartTime("2013-05-04 09:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 11:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00134");
    info.setTrainTypeName("DongCheOne");
    info.setRouteId("8d3c4ec0-f55a-42d3-9cf8-69065c5b1071");
    info.setStartStationName("jiaxingnan");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("taiyuan");
    info.setStartTime("2013-05-04 10:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 12:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00135");
    info.setTrainTypeName("GaoTieOne");
    info.setRouteId("6e967bbb-6f3c-42dd-9d06-0dd048604f93");
    info.setStartStationName("jiaxingnan");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("nanjing");
    info.setStartTime("2013-05-04 11:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 13:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00136");
    info.setTrainTypeName("GaoTieTwo");
    info.setRouteId("11fcc477-52d5-42ee-8485-6e3974741054");
    info.setStartStationName("jiaxingnan");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("wuxi");
    info.setStartTime("2013-05-04 12:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 14:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00137");
    info.setTrainTypeName("DongCheOne");
    info.setRouteId("3017a447-23ff-465b-845d-266ca95dc48b");
    info.setStartStationName("jiaxingnan");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("suzhou");
    info.setStartTime("2013-05-04 13:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 15:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00138");
    info.setTrainTypeName("GaoTieOne");
    info.setRouteId("33757ec5-426e-4cfe-b6fc-10a1567cd9a8");
    info.setStartStationName("jiaxingnan");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("shanghaihongqiao");
    info.setStartTime("2013-05-04 14:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 16:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00139");
    info.setTrainTypeName("GaoTieTwo");
    info.setRouteId("5eedd3a0-1612-4678-a0e0-64b1075f4262");
    info.setStartStationName("jiaxingnan");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("beijing");
    info.setStartTime("2013-05-04 15:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 17:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00140");
    info.setTrainTypeName("DongCheOne");
    info.setRouteId("e1956040-eb80-447d-be10-f790c0d7043e");
    info.setStartStationName("jiaxingnan");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("shijiazhuang");
    info.setStartTime("2013-05-04 16:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 18:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00141");
    info.setTrainTypeName("GaoTieOne");
    info.setRouteId("56acad52-7e71-4c45-85b0-d09d6968e117");
    info.setStartStationName("jiaxingnan");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("xuzhou");
    info.setStartTime("2013-05-04 17:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 19:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00142");
    info.setTrainTypeName("GaoTieTwo");
    info.setRouteId("dcdec1c4-ac9e-4e2d-9e13-bf65ddb20f97");
    info.setStartStationName("jiaxingnan");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("jinan");
    info.setStartTime("2013-05-04 18:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 20:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00143");
    info.setTrainTypeName("DongCheOne");
    info.setRouteId("2599765d-c30b-491b-b380-212f6208f6bb");
    info.setStartStationName("jiaxingnan");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("hangzhou");
    info.setStartTime("2013-05-04 19:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 21:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00144");
    info.setTrainTypeName("GaoTieOne");
    info.setRouteId("a2de26de-6059-4535-8ae0-dc5da94e6a80");
    info.setStartStationName("jiaxingnan");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("zhenjiang");
    info.setStartTime("2013-05-04 08:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 10:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00145");
    info.setTrainTypeName("GaoTieTwo");
    info.setRouteId("a95c23df-9bd2-484b-b1fb-101b4d21123b");
    info.setStartStationName("zhenjiang");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("shanghai");
    info.setStartTime("2013-05-04 09:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 11:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00146");
    info.setTrainTypeName("DongCheOne");
    info.setRouteId("29617239-fb95-434d-b1f0-241a502688cb");
    info.setStartStationName("zhenjiang");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("taiyuan");
    info.setStartTime("2013-05-04 10:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 12:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00147");
    info.setTrainTypeName("GaoTieOne");
    info.setRouteId("e25ca78d-bdc0-48e4-b912-e6711e825ad4");
    info.setStartStationName("zhenjiang");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("nanjing");
    info.setStartTime("2013-05-04 11:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 13:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00148");
    info.setTrainTypeName("GaoTieTwo");
    info.setRouteId("a1202a55-cec2-4dcc-8aa7-e9905f72d216");
    info.setStartStationName("zhenjiang");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("wuxi");
    info.setStartTime("2013-05-04 12:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 14:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00149");
    info.setTrainTypeName("DongCheOne");
    info.setRouteId("89bd0c9e-5663-4717-bf5a-017d264d7f86");
    info.setStartStationName("zhenjiang");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("suzhou");
    info.setStartTime("2013-05-04 13:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 15:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00150");
    info.setTrainTypeName("GaoTieOne");
    info.setRouteId("cd3831fd-b1de-44ca-80f3-b6177a39b4ae");
    info.setStartStationName("zhenjiang");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("shanghaihongqiao");
    info.setStartTime("2013-05-04 14:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 16:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00151");
    info.setTrainTypeName("GaoTieTwo");
    info.setRouteId("1eb5e17d-a77b-4062-8a75-82b4ecaf3061");
    info.setStartStationName("zhenjiang");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("beijing");
    info.setStartTime("2013-05-04 15:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 17:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00152");
    info.setTrainTypeName("DongCheOne");
    info.setRouteId("8cb8c010-aa19-4056-9a33-4da67e30bafa");
    info.setStartStationName("zhenjiang");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("shijiazhuang");
    info.setStartTime("2013-05-04 16:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 18:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00153");
    info.setTrainTypeName("GaoTieOne");
    info.setRouteId("a20069dd-c50d-4970-b591-8b33abb74873");
    info.setStartStationName("zhenjiang");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("xuzhou");
    info.setStartTime("2013-05-04 17:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 19:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00154");
    info.setTrainTypeName("GaoTieTwo");
    info.setRouteId("48d624f7-a36d-4b38-8b5b-2e9fd6d7c44f");
    info.setStartStationName("zhenjiang");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("jinan");
    info.setStartTime("2013-05-04 18:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 20:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00155");
    info.setTrainTypeName("DongCheOne");
    info.setRouteId("d6c76598-be39-460f-a3dc-0db4a27c64eb");
    info.setStartStationName("zhenjiang");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("hangzhou");
    info.setStartTime("2013-05-04 19:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 21:00:00"); //NOSONAR
    service.create(info, null);


    info.setTripId("00156");
    info.setTrainTypeName("GaoTieOne");
    info.setRouteId("c68fe0a0-5143-442a-b93b-4ea6c92f6a54");
    info.setStartStationName("zhenjiang");
    info.setStationsName("intermediatestation");
    info.setTerminalStationName("jiaxingnan");
    info.setStartTime("2013-05-04 08:00:00"); //NOSONAR
    info.setEndTime("2013-05-04 10:00:00"); //NOSONAR
    service.create(info, null);

    }
}
