//! APB_MODULE: Slave Type
//! Simple APB module that behaves as SLAVE. The internal FSM is made by 2 Main Processes
//! First one:  State changing on Clock (Back to IDLE in case of RESET). The reset condition
//!             could be either SYNC or ASYNC with the main clock
//! Second one: State transition and evaluation
//! One quick note on thhe Slave Error signal usually is an output. But the Slave has no concept of 
//! error since there is no error condition in it simply drives signals hence the slaverror is tied 
//! to an input driven by the module where this module is instatiated

/** Time Scale */
`timescale 1ns/1ns

module apb_slave #(
    // Parameters
    parameter DATA_WIDTH = 32,  //! 
    parameter ADDR_WIDTH = 5,   //! 
    parameter WAIT_SATES = 0,   //! 
    parameter SYNC_PROC  = 0,   //! 
    parameter TIEOFF_ERR = 0    //!
) (
    // Input ports
    input logic                     apb_clock,      //!
    input logic                     apb_ares,       //!
    input logic                     apb_psel,       //!
    input logic                     apb_pwrite,     //!
    input logic                     apb_penable,    //!
    input logic [ADDR_WIDTH-1:0]    apb_addr,       //!
    input logic [DATA_WIDTH-1:0]    apb_wdata,      //!
    input logic                     apb_prot,       //!
    input logic                     apb_strb,       //!
    // Output ports
    output logic [DATA_WIDTH-1:0]   apb_rdata,      //!
    output logic                    apb_slverror,   //!
    output logic                    apb_pready,     //!
    // Port forwarding (we do not need the ready)
    output logic                    fwrite,         //!
    output logic                    fenable,        //!
    output logic [ADDR_WIDTH-1:0]   faddr,          //!
    output logic [DATA_WIDTH-1:0]   fwdata,         //!
    output logic                    fprot,          //!
    input logic [DATA_WIDTH-1:0]    frdata,         //!
    input logic                     fslverror       //!
);
    
    /** Parameter checks */
    initial begin
        assert (DATA_WIDTH != 0) else $error("DATA_WIDTH cannot be 0"); 
        assert (ADDR_WIDTH != 0) else $error("ADDR_WIDTH cannot be 0"); 
    end

    /** Internal signals and states */
    typedef enum logic [2:0] {
        IDLE    = 0,
        SETUP   = 1,
        ACCESS  = 2,
        ERROR   = 3
    } apb_slave_state_t;

    apb_slave_state_t cState, nState;

    /** Internal FSM State change */
    generate
        if(SYNC_PROC) begin: sync_proc_state_change
            always_ff @(posedge apb_clock) begin
                if(apb_ares) begin
                    cState <= IDLE;
                end else begin
                    cState <= nState;
                end
            end
        end
        else begin: async_proc_state_change
            always_ff @(posedge apb_clock or posedge apb_ares) begin
                if(apb_ares) begin
                    cState <= IDLE;
                end else begin
                    cState <= nState;
                end
            end            
        end
    endgenerate
    
    /** Pready Controller:
        Pready is High when:
        1 -> We are in Access Phase, since that would mean the SLAVE will answer in the immediate next clock cycle
        2 -> In all other states Pready must be 0 expecially in case of WAIT STATES transfer
    */
    assign apb_pready = (nState == ACCESS);

    /** WAIT states counter */
    logic [WAIT_SATES:0] waitingCNT;
    logic CNTdone;
    always_ff @(posedge apb_clock or posedge apb_ares) begin: waiting_counter
        if(apb_ares)    waitingCNT <= 0;
        else            waitingCNT <= waitingCNT + 1;
    end
    assign CNTdone = (waitingCNT == WAIT_SATES);

    /** Internal Main FSM */
    /** 
        A transfer Happanes once the PSEL is 1 
        A No Transfer happanes once the PSEL = 0 and PENABLE is 0 
    */    
    always_comb begin: state_computation_proc
        case (cState)
            IDLE:   begin: idle_state
                if((apb_psel == 0) && (apb_penable == 0)) begin
                    nState  = IDLE;
                end else if((apb_psel == 1) && (apb_penable == 0)) begin
                    nState  = SETUP;
                end else begin
                    nState  = IDLE;
                end
            end
            SETUP:  begin: setup_state
                if((apb_psel == 1) && (apb_penable == 0) && (CNTdone == 0)) begin
                    nState  = SETUP;
                end else if((apb_psel == 1) && (apb_penable == 1)) begin
                    nState  = ACCESS;
                end else begin
                    nState  = ERROR;
                end
            end
            ACCESS: begin: access_state
                if((apb_penable == 0) && (apb_psel == 1)) begin
                    nState  = SETUP;
                end else if((apb_penable == 0) && (apb_psel == 0)) begin
                    nState  = IDLE;
                end else begin
                    nState  = ERROR;
                end
            end
            default: begin
                nState = IDLE;
            end
        endcase
    end

    /** Internal Port Forwarding Driver */
    always_comb begin: port_forwarding_proc
        case (cState)
            IDLE:   begin: idle_state
                /** all the output ports are Set to 0 */
                fwrite      = 0;
                fenable     = 0;
                faddr       = 0;
                fwdata      = 0;
                apb_rdata   = 0;
            end
            SETUP:  begin: setup_state
                /** the setup is where we can forward the WDATA - WRITEOP - ADDR */
                faddr   = apb_addr;
                fwrite  = apb_pwrite;
                fwdata  = apb_wdata;
                fenable = apb_penable;
            end
            ACCESS: begin: access_state
                /** in access Phase we assume the PENABLE is high hence we can select the FAN OUT slave. The read data will
                    be transfered only when we know the pready is 1 again since it means the tramsfered is completed 
                    and we can go back to setup. If the FAN OUT slave takes more than a CYCLE we need to stich a wait STATE */
                apb_rdata   = frdata;
                fenable     = apb_penable;
            end
            default: begin
                /** In Error state we drive everything to 0 */
                fwrite      = 0;
                fenable     = 0;
                faddr       = 0;
                fwdata      = 0;
                apb_rdata   = 0;
            end
        endcase
    end

    /** Prot is the only directly forwarded port */
    assign fprot        = apb_prot;

    /** Error case, when in ERROR we do not hang till new reset, error will last 1 cycle*/
    generate
        if(TIEOFF_ERR) begin: error_tied_off
            assign apb_slverror = 0;
        end else begin: error_not_tied_off
            assign apb_slverror = (cState == ERROR) | fslverror;
        end
    endgenerate
endmodule // apb_slave