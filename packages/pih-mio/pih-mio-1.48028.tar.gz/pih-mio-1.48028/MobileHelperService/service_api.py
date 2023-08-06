import importlib.util
import sys
from collections import defaultdict
from threading import Thread

pih_is_exists = importlib.util.find_spec("pih") is not None
if not pih_is_exists:
    sys.path.append("//pih/facade")
from pih import A
from typing import Callable, Any

SR = A.CT_SR
SC = A.CT_SC

ROLE: SR = SR.MOBILE_HELPER

#version 0.8

AS_DEVELOPER_ALIAS: str = "as_developer"

def as_developer() -> bool:
    return A.SE.named_arg(AS_DEVELOPER_ALIAS)

class MobileHelperService():

    INIT: bool = False
    INSTANCE: Any | None = None
    NAME: str = "MobileHelper"
   
    sender_profile_id: A.CT_ME_WH_W.Profiles = A.ME_WH_W.get_profile_id(A.D_TN.it_administrator())

    if A.U.update_for_service(ROLE):
        from pih import PIH, Stdin, NotFound, SubscribtionResult
        from pih.tools import ParameterList, BitMask as BM
        from pih.collection import WhatsAppMessage, User
        from MobileHelperService.api import (MobileHelper as Api, MobileSession, MobileOutput, 
                        MobileInput, MobileUserInput, MobileMarkInput, 
                        InternalInterrupt, AddressedInterruption, Flags)
        
        INIT = True

    mobile_helper_client_map: dict[str, Api] = {}

    def __init__(self, max_client_count: int, checker: Callable[[str], bool] | None = None):
        self.max_client_count = max_client_count
        self.root: str = self.PIH.NAME
        self.checker = checker
        self.service_role: SR = SR.MOBILE_HELPER
        self.allow_send_to_next_service_in_chain: dict[str, bool] = defaultdict(bool)
        MobileHelperService.INSTANCE = self  
           
    def start(self) -> bool:
        if MobileHelperService.INIT:
            A.SE.add_arg(AS_DEVELOPER_ALIAS,
                    nargs="?", const=1, type=str, default=None)
            service_role_desctiption: self.ServiceRoleDescription | None = A.SRV_A.create_support_service_or_master_service_description(A.CT_SR.description(self.service_role))
            if not A.D_C.empty(service_role_desctiption):
                with A.ER.detect_interruption("Выход"):
                    A.SRV_A.serve(service_role_desctiption, self.service_call_handler,
                                MobileHelperService.service_starts_handler)
                return True
        return False

    def create_mobile_helper(self, telephone_number: str, flags: int | None = None, recipient: str | None = None) -> Api:
        stdin: self.Stdin = self.Stdin()
        session: self.MobileSession = self.MobileSession(telephone_number, flags)
        output: self.MobileOutput = self.MobileOutput(session)
        session.say_hello(recipient)
        input: self.MobileInput = self.MobileInput(
            stdin, self.MobileUserInput(), self.MobileMarkInput(), output, session)
        return self.Api(self.PIH(input, output, session), stdin)

    @staticmethod
    def say_good_bye(mobile_helper: Api) -> str:
        mobile_helper.say_good_bye()

    def pih_handler(self, telephone_number: str, line: str | None = None, sender_user: User | None = None, flags: int | None = 0, chat_id: str | None = None) -> None:  
        mobile_helper: self.Api | None = None
        while True:
            try:
                if MobileHelperService.is_client_new(telephone_number):
                    A.IW.remove(A.CT.MOBILE_HELPER.POLIBASE_PERSON_PIN, telephone_number)
                    if self.Api.check_for_starts_with_pih_keyword(line):
                        self.allow_send_to_next_service_in_chain[telephone_number] = self.is_client_stack_full() 
                        if not self.allow_send_to_next_service_in_chain[telephone_number]:
                            MobileHelperService.mobile_helper_client_map[telephone_number] = self.create_mobile_helper(telephone_number, flags, chat_id)
                    else:
                        self.allow_send_to_next_service_in_chain[telephone_number] = False
                else:
                    self.allow_send_to_next_service_in_chain[telephone_number] = False
                if telephone_number in MobileHelperService.mobile_helper_client_map:
                    mobile_helper = MobileHelperService.mobile_helper_client_map[telephone_number]
                    show_good_bye: bool = mobile_helper.level == 0
                    if self.Api.check_for_starts_with_pih_keyword(line):
                        mobile_helper.level = 0
                    if mobile_helper.do_pih(line, sender_user, flags):
                        if show_good_bye and mobile_helper.level <= 0:
                            if A.D.is_none(flags) or not self.BM.has(flags, self.Flags.SILENCE):
                                MobileHelperService.say_good_bye(mobile_helper)
                break
            except self.NotFound:
                break
            except self.InternalInterrupt as interruption:
                if interruption.type == A.CT.MOBILE_HELPER.InteraptionTypes.INTERNAL:
                    line = mobile_helper.line
                    if not self.Api.check_for_starts_with_pih_keyword(line):
                        MobileHelperService.say_good_bye(mobile_helper)
                        break
                else:
                    MobileHelperService.say_good_bye(mobile_helper)
                    break

    def is_client_stack_full(self) -> bool:
        return len(MobileHelperService.mobile_helper_client_map) == self.max_client_count

    def is_client_new(value: str) -> bool:
        return value not in MobileHelperService.mobile_helper_client_map

    def receive_message_handler(self, message_text: str, telephone_number: str, flags: int | None = None, chat_id: str | None = None) -> None:
        interruption: self.AddressedInterruption | None = None
        while True:
            try:
                if A.D_C.empty(interruption):
                    self.pih_handler(telephone_number, message_text, None, flags, chat_id)
                else:
                    for recipient_user in interruption.recipient_user_list():
                        recipient_user: self.User = recipient_user
                        self.pih_handler(recipient_user.telephoneNumber, " ".join(
                            [self.root, interruption.command_name]), interruption.sender_user, interruption.flags)
                    interruption = None
                break
            except self.AddressedInterruption as local_interruption:
                interruption = local_interruption

    def receive_message_handler_thread_handler(self, message: WhatsAppMessage) -> None:
        self.receive_message_handler(message.message, message.sender, None, message.chatId)

    def service_call_handler(self, sc: SC, parameter_list: ParameterList, subscribtion_result: SubscribtionResult | None) -> Any:
        if sc == A.CT_SC.send_event:
            if A.D.is_not_none(subscribtion_result) and subscribtion_result.result:
                if subscribtion_result.type == A.CT_SubT.ON_RESULT_SEQUENTIALLY:
                    message: self.WhatsAppMessage | None = A.D_Ex_E.whatsapp_message(
                        parameter_list)
                    if A.D.is_not_none(message):
                        if A.D.get_by_value(A.CT_ME_WH_W.Profiles, message.profile_id) == A.CT_ME_WH_W.Profiles.IT:
                            allow_in_group: bool = not A.D_C.empty(message.chatId) and message.chatId in [A.D.get(A.CT_ME_WH.GROUP.IT)]
                            if A.D.is_none(message.chatId) or allow_in_group:
                                telephone_number: str = message.chatId if allow_in_group else message.sender
                                if allow_in_group:
                                    message.chatId = message.sender
                                    message.sender = telephone_number
                                if A.D.is_none(self.checker) or self.checker(telephone_number):
                                    if self.is_client_stack_full():
                                        return True
                                    else:
                                        if telephone_number in self.allow_send_to_next_service_in_chain:
                                            del self.allow_send_to_next_service_in_chain[telephone_number]
                                        Thread(target=self.receive_message_handler_thread_handler, args=[message]).start()
                                        while telephone_number not in self.allow_send_to_next_service_in_chain:
                                            pass
                                        return self.allow_send_to_next_service_in_chain[telephone_number]
                                else:
                                    if telephone_number in MobileHelperService.mobile_helper_client_map:
                                        del MobileHelperService.mobile_helper_client_map[telephone_number]
                                    return True
            return False
        if sc == A.CT_SC.send_mobile_helper_message:
            self.receive_message_handler(
                " ".join((self.root, parameter_list.next())), parameter_list.next(), parameter_list.next())
        return None

    @staticmethod
    def service_starts_handler() -> None:
        if as_developer():
            A.O.blue("As developer")
        A.SRV_A.subscribe_on(A.CT_SC.send_event, A.CT_SubT.ON_RESULT_SEQUENTIALLY, MobileHelperService.NAME)